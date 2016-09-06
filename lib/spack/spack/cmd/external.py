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
import spack
from spack.build_environment import create_module_cmd
import spack.cmd
import spack.config
from spack.spec import Spec


description = "Create an external spec from a given module name"


def setup_parser(subparser):
    """Can enter either via path or module name. Compiler spec should be
       provided """

    subparser.add_argument("package_name", 
                           help="supply the base name for package")
    subparser.add_argument("-p", "--path", help="supply path")
    subparser.add_argument("-m","--module", 
                           help="supplied name is a module name")
    subparser.add_argument("cspec", nargs="+", help="compiler spec to use")


def external(subparser, args):
    specs_dict = {}
    external, external_type =  "", "" 

    matches = get_versions_from_args(args) # Find versions from mod or path
    name = get_package_name(matches) 
    version_list = get_version_list(matches) 

    if args.module:
        external = args.module
        external_type = "modules"
    else:
        external = args.path
        external_type = "paths"

    for v in version_list:
        specs_dict.update(_create_yaml_dict(name, v, args.cspec, external))
    
    yaml_entry = _create_json_entry(name, specs_dict, external_type)
    spack.config.update_config("packages", yaml_entry)


def get_package_name(match_list):
    return match_list[0]


def get_version_list(match_list):
    return match_list[1]


def get_versions_from_args(args):
    matches = []
    if args.module:
        matches = _get_versions_from_modules(args)
    else:
        matches = _get_versions_from_path(args)
    return matches


def _get_versions_from_modules(args):
    modulecmd = create_module_cmd()
    matches = [args.package_name]
    output = modulecmd("avail", args.module, output=str, error=str)
    module_regex = r'{0}/([.\d]+)'.format(args.module)
    version_list = re.findall(module_regex, output)
    matches.append(version_list)
    return matches


def _get_versions_from_path(args):
    matches = [args.package_name]
    version_list = []
    external_path = args.path

    base_name = os.path.basename(external_path)
    # Need a way to check various different ways versions could exist via
    # a path. 
    dir_list = _first_level_directory(external_path)

    for ver in dir_list:
        if _represents_string_version(ver):
            version_list.append(ver)
    matches.append(version_list)
    return matches

def _first_level_directory(path):
    """Get the first level of a directory """
    return os.walk(path).next()[1]


def _represents_string_version(dirname):
    """ Check if directory name follows a version number """
    # Kinda hacky since we assume that versions just have period delimiters
    try:
        stripped = dirname.strip(".")
        int(stripped[0])
        return True
    except ValueError:
        return False
    

def _create_yaml_dict(name, version, cspec, external):
    """ Create specs from the base_name, version and compiler specs added """
    package_specs = {}
    for c in cspec:
        spec_string = "{0}@{1}{2}".format(name, version, c)
        package_specs[spec_string] = external

    return package_specs


def _create_json_entry(base_name, specs, external_type):
    """ Create a json entry that we can simply append or create the json
    file to append to."""
    module_dict = {}      
    module_dict[base_name] = {"buildable": False, external_type : {}}
    module_dict[base_name][external_type].update(specs)
    return module_dict
