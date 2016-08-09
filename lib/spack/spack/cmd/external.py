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
import re
import spack
from spack.build_environment import create_modulecmd
import spack.cmd
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
    for name, version, default in matches:
        specs.extend(create_specs(name, version, args.cspec))
    # Output to stdout because it would also be cool for people to see what
    # Is being written


def grep_for_package_name(args):
    modulecmd = create_modulecmd()

    if args.module:
        external_name = args.module
        output = modulecmd("avail", external_name, output=str, error=str)
        module_regex = r'({0})/([.\d]+)(\(default\))?'.format(external_name)
        matches = re.findall(module_regex, output)
    
    elif args.path:
        external_name = args.path
    
    return matches


def create_specs(name, version, cspec):
    package_specs = []
    for c in cspec:
        spec_string = "{0}@{1}{2}".format(name, version, c)
        spec = Spec(spec_string)
        spec.concretize()
        package_specs.append(spec)
    return package_specs


def create_json_entry(name, version):
    """ Create a json entry that we can simply append or create the json
    file to append to. Some helper functions might already exist for the
    creation
    """
    pass
