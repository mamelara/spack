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
    matches = grep_for_package_name(args) # Grep for either path or module
    specs = []
    for name, version in matches:
        specs.extend(create_specs(name, version, args.cspec))
    # Output to stdout because it would also be cool for people to see what
    # Is being written
    modules = True

    if args.paths:
        modules = False

    yaml_entry = create_json_entry(args.package_name, specs, modules)
    spack.config.update_config("packages", yaml_entry)


def grep_for_package_name(args):
    modulecmd = create_module_cmd()

    if args.module:
        external_name = args.module
        output = modulecmd("avail", external_name, output=str, error=str)
        module_regex = r'({0})/([.\d]+)'.format(external_name)
        #module_regex = r'({0})/([.\d]+)(\(default\))?'.format(external_name)
        matches = re.findall(module_regex, output)
    
    elif args.path: # Need to some how work through the path
        matches = []
        external_path = args.path
        base_name = os.path.basename(external_path)
        dir_list = first_level_directory(external_path)
        for ver in dir_list:
            if represents_string_version(ver):
                matches.append((base_name, ver)) 
    
    return matches


def get_versions(path):
    """Check if path name has a version attached to it. If so grab it for
       creating the spec """
    pass


def first_level_directory(path):
    """Get the first level of a directory """
    return os.walk(path).next()[1]


def represents_string_version(dirname):
    """ Check if directory name follows a version number """
    # Kinda hacky since we assume that versions just have period delimiters
    try:
        stripped = dirname.strip(".")
        int(stripped[0])
        return True
    except ValueError:
        return False
    

def create_specs(name, version, cspec):
    """ Create specs from the base_name, version and compiler specs added """
    package_specs = []

    for c in cspec:
        spec_string = "{0}@{1}{2}".format(name, version, c)
        spec = Spec(spec_string)
        spec.concretize()
        package_specs.append((spec, name))

    return package_specs


def create_json_entry(base_name, list_of_specs, modules):
    """ Create a json entry that we can simply append or create the json
    file to append to."""
    external_type = "modules"

    if not modules:
        external_type = "paths"

    module_dict = {}      
    module_dict[base_name] = {"buildable": False, external_type : {}}

    for s, name in list_of_specs:
        module_dict[base_name][external_type].update({str(s) : name})

    return module_dict
