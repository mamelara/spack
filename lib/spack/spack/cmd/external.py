##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import argparse
import os
import re

import llnl.util.tty as tty
from llnl.util.tty.colify import colify
import spack
from spack.build_environment import create_module_cmd
import spack.cmd
import spack.compilers
import spack.config
from spack.external_package import ExternalPackage
import spack.error
from spack.util.spack_yaml import syaml_dict
from spack.spec import Spec

description = "Add an external package entry to packages.yaml"


def setup_parser(subparser):
    """
    Sets up parser for external add and external rm. The arguments are as
    follows:
        spack external add [package_spec] [path or module]  
    """      
    scopes = spack.config.config_scopes
    # Set up subcommands external and rm
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", 
                                  dest = "external_command")
    # external add
    add_parser = sp.add_parser(
            'add', help="Add packages to Spack's config file")
    add_parser.add_argument("package_spec",
                            help="spec for external package")
    add_parser.add_argument("external_location",
                            help="path or module (location) of external pkg")
    add_parser.add_argument("--scope", choices=scopes,
                            default=spack.cmd.default_modify_scope,
                            help="Configuration scope to modify.")

    rm_parser = sp.add_parser('rm', help="Delete an entry from packages.yaml")
    rm_parser.add_argument("package_spec",
                           help="spec of a package to delete")
    rm_parser.add_argument("--scope", choices=scopes,
                           default=spack.cmd.default_modify_scope,
                           help="Configuration scope to modify.")


def duplicate_specs(spec, specs_from_yaml):
    """ Checks to see if an entry from a yaml contains the same spec
        Returns true iff there is a spec match, else false"""
    for k in specs_from_yaml.keys():
        if Spec(k) == spec:
            return True
    return False


def get_specs_from_package_yaml(package, ext_type):
    """ Returns the specs dictionary of a package entry """
    return package.get(ext_type, {})


def output_successful_addition_to_yaml(spec):
    """Output message to user when a package is added to the config"""
    tty.msg("Added %s to packages.yaml" % spec)


def add_entry_to_yaml(external_package_config, scope):
    """Adds a completely new entry to the config file """
    spack.config.update_config("packages", 
                               external_package_config, 
                               scope=scope)



def update_yaml_entry(external_package, package_yaml):

    def update_specs(old_specs, new_spec):
        """ add new spec dict to the old spec dict """
        copy_specs = old_specs.copy()
        copy_specs.update(new_spec)
        package_yaml[external_package.external_type] = copy_specs
        return package_yaml

    external_type = external_package.external_type
    specs_from_yaml = get_specs_from_package_yaml(package_yaml, external_type) 
    updated_package_yaml = update_specs(specs_from_yaml, 
                                        external_package.spec_dict())

    return {external_package.name: updated_package_yaml}
    

def append_to_existing_entry(external_package, package_yaml, scope):
    """Appends spec to an existing package if the spec does not already
    exist"""
    specs_dict = get_specs_from_package_yaml(package_yaml, 
                                             external_package.external_type)

    if not duplicate_specs(external_package.spec, specs_dict):
        updated_package_yaml = update_yaml_entry(external_package, 
                                                 package_yaml)
        add_entry_to_yaml(updated_package_yaml, scope=scope)
        output_successful_addition_to_yaml(str(external_package))
    else:
        tty.msg("Added no new entries to packages.yaml")


def get_external_from_spec(spec, scope):
    package_name = spec.name
    packages = spack.config.get_config("packages", scope=scope)
    return packages.get(spec.name, {})


def add_to_packages_yaml(external_package, scope):
    """Given an external package and scope, add the external package to
       the packages.yaml config file. """

    package_entry_from_yaml = get_external_from_spec(external_package.spec,
                                                     scope)
    if not package_entry_from_yaml:
        add_entry_to_yaml(external_package.to_dict(), scope=scope)
        output_successful_addition_to_yaml(str(external_package))
    else:
        append_to_existing_entry(external_package,
                                package_entry_from_yaml, 
                                scope)
    

def external_add(args):
    """ Find packages and add them to packages.yaml"""
    package_spec = spack.spec.Spec(args.package_spec)
    external_location = args.external_location
    scope = args.scope
    external_package = ExternalPackage.detect_package(package_spec, 
                                                      external_location)
    add_to_packages_yaml(external_package, scope)


def find_specs_and_external_type(package_yaml):
    for ext_type in ["modules", "paths"]:
        specs_section = get_specs_from_package_yaml(package_yaml, ext_type)
        if specs_section:
            return specs_section, ext_type
    return {}, "unknown"


def filter_specs(spec, specs_section):
    return {k: v for k, v in specs_section.items() if Spec(k) != spec}


def remove_package_entry(package_spec, scope):
    packages = spack.config.get_config("packages", scope)
    packages.pop(package_spec.name, None)
    return packages


def write_to_packages_yaml(updated_packages_yaml, scope):
    """Overwrite entire packages yaml file with updated entries.
       The reason for this is that dict.update does not really
       update the config file when an entry is deleted"""
    scope = spack.config.validate_scope(scope)
    scope.sections["packages"] = {"packages": updated_packages_yaml}
    scope.write_section("packages")


def external_rm(args):
    package_spec = spack.spec.Spec(args.package_spec)
    scope = args.scope
    package_yaml = get_external_from_spec(package_spec, scope)
    specs_section, external_type = find_specs_and_external_type(package_yaml)

    if not specs_section:
        tty.die("Could not find package %s in packages.yaml")

    filtered_specs = filter_specs(package_spec, specs_section) 

    if not filtered_specs:
        updated_packages_yaml = remove_package_entry(package_spec, scope)
        write_to_packages_yaml(updated_packages_yaml, scope)
    else:         
        package_yaml[external_type] = filtered_specs
        external_package_config = {package_spec.name : package_yaml}
        add_entry_to_yaml(external_package_config, scope)
        tty.msg("Removed %s from packages.yaml" % package_spec)
    

def external(parser, args):
    action = {"add": external_add,
              "rm" : external_rm }
    action[args.external_command](args)
