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


description = "Create an external spec from a given module name or path"


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


def external_add(args):
    """ Find packages and add them to packages.yaml"""
    package_spec = spack.spec.Spec(args.package_spec)
    external_location = args.external_location
    scope = args.scope
    external_package = ExternalPackage.detect_package(package_spec, 
                                                      external_location)
    add_to_packages_yaml(external_package, scope)

    
def create_yaml_dict(external_package, specs_dict=None):
    """ 
    Packages.yaml entries look like the following: 
        {package_name: 
            buildable : False|True,
            modules|paths:
                spec : module_name | path}
    """ 
    external_type = external_package.external_type
    if not specs_dict:
        specs_dict = {str(external_package): 
                      external_package.external_location}
    package_yaml = syaml_dict([("buildable", False),
                               (external_type, specs_dict),
                               ("version", [str(external_package.version)])])
    return package_yaml


def duplicate_specs(spec, spec_dict):
    for k, v in spec_dict.items():
        if spack.spec.Spec(k) == spec:
            return True
    return False


def get_specs_from_package_yaml(package_dict, ext_type):
    """ Accepts a package_dict with format {"buildable": T|F, 
                                            "modules"|"paths":
                                            {"spec" : "external_location}}
        Returns the spec part of the dictionary
    """
    return package_dict.get(ext_type, {})


def update_yaml_specs(external_package, specs_dict):
    new_spec = {str(external_package): external_package.external_location}
    specs_dict.update(new_spec)
    return specs_dict


def append_to_existing_yaml(external_package, package_from_entry_yaml, scope):
    specs_dict = get_specs_from_package_yaml(package_from_entry_yaml,
                                             external_package.external_type)

    if not duplicate_specs(external_package.spec, specs_dict):
        updated_specs_dict = update_yaml_specs(external_package, specs_dict)
        package_yaml = create_yaml_dict(external_package, updated_specs_dict)
        package_entry = {external_package.name: package_yaml}
        spack.config.update_config("packages", package_entry, scope=scope)


def add_to_packages_yaml(external_package, scope):

    def get_external_from_spec(spec):
        package_name = spec.name
        packages = spack.config.get_config("packages", scope=scope)
        return packages.get(spec.name, {})  

    package_entry_from_yaml = get_external_from_spec(external_package.spec)

    if not package_entry_from_yaml:
        package_yaml = create_yaml_dict(external_package)
        package_entry = {external_package.name: package_yaml}
        spack.config.update_config("packages", package_entry, scope=scope)
    else:
        append_to_existing_yaml(external_package,
                                package_entry_from_yaml, 
                                scope)


def external_rm(args):
    pass


def external(parser, args):
    action = {"add": external_add,
              "rm" : external_rm }
    action[args.external_command](args)
