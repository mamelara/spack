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

import spack
import spack.cmd
from spack.spec import Spec

description = "Create an external spec from a given module name" 

def setup_parser(subparser):
    """Can enter either via path or module name. Compiler spec should be 
       provided """

    subparser.add_argument("path", nargs="?", help="supply path")
    subparser.add_argument("-m","--module", nargs="?", 
                           help="supplied name is a module name")
    subparser.add_argument("cspec", nargs="+", help="compiler spec to use")

def external(parser, args):
    print args.__dict__
    if args.path:
        path = args.path
    elif args.module:
        module = args.module

    if not cspec:
        tty("Please provide a Compiler Spec for the external module")
    pass






