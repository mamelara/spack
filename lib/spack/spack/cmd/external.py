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
import spack.config
import spack.error
from spack.spec import Spec


#USE SPACK.COMPILERS.FIND(SPEC, SCOPE) --> So that people can use args
description = "Create an external spec from a given module name or path"


def setup_parser(subparser):
    """Can enter either via path or module name. Compiler spec should be
       provided """
    scopes = spack.config.config_scopes

    sp = subparser.add_subparsers(metavar="SUBCOMMAND", 
                                  dest = "external_command")
    # external add
    add_parser = sp.add_parser(
            'add', help="Add packages to Spack's config file")
    add_parser.add_argument("-p", "--path", help="supply path of package")
    add_parser.add_argument(
            "-m","--module", help="supply module name for a tcl module")
    add_parser.add_argument(
            "package_name", help="supply the base name for package")
    add_parser.add_argument("cspecs", nargs="+", help="compiler spec to use")
    add_parser.add_argument("--scope", choices=scopes,
                            default=spack.cmd.default_modify_scope,
                            help="Configuration scope to modify.")
    # external remove
    rm_parser = sp.add_parser(
            'remove', aliases=['rm'], help="Remove packages from Spack config file")
    rm_parser.add_argument('-a', '--all', action='store_true',
                           help="Remove entire entry for that external package")
    rm_parser.add_argument("-p", "--paths", action="store_true",
                           help="spec to delete is in paths")
    rm_parser.add_argument("-m", "--modules", action="store_true",
                           help="spec to delete is in modules") 
    rm_parser.add_argument("external_spec")
    rm_parser.add_argument("--scope", choices=scopes, 
                           default=spack.cmd.default_modify_scope,
                           help="Configuration scope to modify.")

def external_add(args):
    check_valid_input(args) # Check whether we are missing any pos arguments
    external_name, external_type =  "", "" 
    found_versions = find_versions_from_args(args) # Find versions from mod or path
    
    # Assign to external either the module name or the path to a external pkg
    # Change external_type to the correct label according to user args
    if args.module:
        external_name = args.module  #
        external_type = "modules"
    else:
        external_name = args.path
        external_type = "paths"

    # Collect all information needed to create packages.yaml entries
    # And put into a container
    package_info = collect_package_info(args, external_name, external_type)
    package_yaml = create_yaml_dict(package_info, found_versions)
    add_to_packages_yaml(package_yaml, package_info, args.scope)


def collect_package_info(args, external_name, external_type):
    package_name = args.package_name
    cspecs = args.cspecs
    return {"package_name": package_name,
            "external_name": external_name,
            "external_type": external_type,
            "cspec": cspecs}


def get_package_name(package):
    return package["package_name"]


def get_external_name(package):
    return package["external_name"]


def get_external_type(package):
    return package["external_type"]


def get_compiler_specs(package):
    return package["cspec"]


def find_versions_from_modules(args):
    """ Helper to find versions via modules """
    package_name = args.package_name
    modulecmd = create_module_cmd()
    matches = {}
    output = modulecmd("avail", args.module, output=str, error=str)
    module_regex = r'{0}/([.\d]+)'.format(args.module)
    version_list = re.findall(module_regex, output)
    return version_list
    

def get_directory_names_from_path(path):
    """Get the first level of a directory and return a list
       of the filenames""" 
    dir_list = os.walk(path).next()[1]
    dir_list.append(os.path.basename(path))
    return dir_list


def represents_string_version(dirname):
    """ Check if directory name follows a version number """
    try:
        ver = dirname.split(".")
        int(ver[0])
        return True
    except ValueError:
        return False


def extract_version_from_string(dirname):
    """Extract the version from a given string but check first
       if it is a valid version string"""
    ver = ""
    if "-" in dirname:
        file_list = dirname.split("-")
        ver = file_list[1]  # in case we have a package-ver dir name
    elif "." in dirname:
        ver = dirname  # We probably have a version string

    if represents_string_version(ver):
        return ver
    else:
        return None


def find_versions_from_path(args):
    """ Helper to find versions via paths """
    package_name = args.package_name
    matches = {}
    version_list = []
    external_path = args.path
    dir_list = get_directory_names_from_path(external_path)
    for v in dir_list:
        ver = extract_version_from_string(v)
        if ver:
            version_list.append(ver)
    return version_list


def find_versions_from_args(args):
    """ Calls two helper methods to find versions either using
        modules or a path depending on the argument provided by user """
    matches = None
    if args.module:
        matches = find_versions_from_modules(args)
    else:
        matches = find_versions_from_path(args)
    return matches


def check_valid_input(args):
    """ Check for valid input. Throw error in case we received incorrect
    args """
    package_name = args.package_name
    if not package_name.isalnum():
        #TODO: Change it to something nicer than throwing a stack trace
        raise ValueError("Did not receive valid input for package_name")


def create_specs(package_name, found_versions, external, cspec):
    package_specs = {}
    for v in found_versions:
        for c in cspec:
            spec_string = "{0}@{1}{2}".format(package_name, v, c)
            package_specs[spec_string] = external
    return package_specs    


def create_yaml_dict(package_info, versions):
    """ Create specs from the package name, version and compiler specs added """

    external_name = get_external_name(package_info)
    package_name = get_package_name(package_info)
    external_type = get_external_type(package_info)
    compiler_specs = get_compiler_specs(package_info)

    spec_entries = create_specs(package_name, 
                                versions, 
                                external_name, 
                                compiler_specs)
    package_dict = {"buildable" : False, external_type : spec_entries}
    return package_dict


def filter_duplicate_specs(package_specs, yaml_specs):
    return {k : v for k, v in package_specs.items() 
            if k not in yaml_specs.keys()}


def get_external_specs(package, external_type):
    return package[external_type]


def get_specs_from_yaml(packages_yaml, package_name, external_type):
    return packages_yaml.get(package_name, {}).get(external_type, {})


def add_to_packages_yaml(package_yaml, package_info, scope):
    """ Adds to packages.yaml. First checks if an entry exists if not then we
    just add to the package, else we filter. """
    package_name = get_package_name(package_info)
    external_type = get_external_type(package_info)
    packages = get_packages_yaml_config(scope)

    specs_from_yaml = get_specs_from_yaml(packages, package_name, external_type)
    new_specs = get_external_specs(package_yaml, external_type)
    external_specs = filter_duplicate_specs(new_specs, specs_from_yaml)

    if external_specs:
        package = {package_name : {}}
        package_yaml[external_type].update(external_specs)
        n = len(external_specs.keys())
        s = 's' if n > 1 else ''
        filename = spack.config.get_config_filename(scope, "packages")
        tty.msg("Added %d new package%s to %s" % (n, s, filename))
        package[package_name] = package_yaml
        spack.config.update_config("packages", package, scope=scope)
    else:
        tty.msg("Added no new packages")


def get_external_type_from_args(args):
    if args.modules:
        return "modules"
    else:
        return "paths"


def remove_spec_entry(specs_dict, spec):
    return {k : v for k, v in specs_dict.items() 
            if not Spec(k).satisfies(spec)}


def external_rm(args):
    external_type = get_external_type_from_args(args)
    packages_yaml = get_packages_yaml_config(args.scope)
    package_spec = Spec(args.external_spec)
    package_name = package_spec.name
    external_package = packages_yaml.get(package_name, {})
    
    if not external_package:
        tty.die("No external_packages match spec %s" % package_spec)
    elif args.all: # delete the entire section
        del packages_yaml[package_name][external_type] 
        spack.config.update_config("packages", packages_yaml, 
                                   scope=args.scope)
    else: 
        specs_dict = external_package.get(external_type, {})
        if specs_dict:
            filtered_config = remove_spec_entry(specs_dict, package_spec)
            if len(filtered_config.keys()) == len(specs_dict.keys()):
                raise PackageSpecInsufficientlySpecificError(package_spec)

            packages_yaml[package_name][external_type] = filtered_config
            spack.config.update_config("packages", 
                                       packages_yaml, 
                                       scope=args.scope)
            tty.msg("Removed package spec %s" % package_spec)


def get_packages_yaml_config(scope=None):
    return spack.config.get_config("packages", scope=scope)


def external(parser, args):
    action = {"add": external_add,
              "rm" : external_rm }
    action[args.external_command](args)


class PackageSpecInsufficientlySpecificError(spack.error.SpackError):
    def __init__(self, package_spec):
        super(PackageSpecInsufficientlySpecificError, self).__init__(
                "Multiple external packages satisfy spec %s" % package_spec)
