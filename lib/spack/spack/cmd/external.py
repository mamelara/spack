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
import spack.error
from spack.spec import Spec


description = "Create an external spec from a given module name or path"


def setup_parser(subparser):
    """
    Sets up parser for external add and external rm. The arguments are as
    follows:

        spack external add [package_name] [-m|-p] [module_name|path_name] ...
        
        additional args include:
        cspecs    - User inputs a compiler spec to create the external entry
        variant   - optional argument for variant

        The user enters a package name (a common package name i.e hdf5) 
        and then provides either the -m or -p flag along with either
        module name or path. The external module will then parse output
        from the module avail command or search the directory tree for
        versions.

        spack external rm [-a|--all] [-p|-m] package_spec

        The user enters enters an optional flag -a for all or can 
        provide a flag -p or -m  to remove an entry in either modules
        or paths, if it is present. They provide a spec to match entries to 
        be deleted.
    """      
    scopes = spack.config.config_scopes

    # Set up subcommands external and rm
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
    add_parser.add_argument("-v", "--variant", 
                            help="supply variant for package")
    add_parser.add_argument("--scope", choices=scopes,
                            default=spack.cmd.default_modify_scope,
                            help="Configuration scope to modify.")
    # external remove
    rm_parser = sp.add_parser('remove', aliases=['rm'], 
                              help="Remove packages from Spack config file")
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
    found_versions = find_versions_from_args(args)
    
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
    """Container for relevant information to create packages.yaml entries """
    package_name = args.package_name
    cspecs = args.cspecs
    return {"package_name": package_name,
            "external_name": external_name,
            "external_type": external_type,
            "cspec": cspecs,
            "variant": args.variant}


# Below are getters for package information.
def get_package_name(package):
    return package["package_name"]


def get_external_name(package):
    return package["external_name"]


def get_external_type(package):
    return package["external_type"]


def get_compiler_specs(package):
    return package["cspec"]


def get_variant_spec(package):
    return package["variant"]


def find_versions_from_modules(args):
    """ Helper to find versions via modules. Uses module cmd and
        then greps output for relevant package name"""
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


def get_operating_system_from_compiler_spec(compiler_spec):
    compilers = spack.compilers.compiler_for_spec(compiler_spec.strip("%"))
    return str(compilers[0].operating_system)


def replace_os_in_arch_string(arch_string, compiler_spec):
    os_string = get_operating_system_from_compiler_spec(compiler_spec)
    arch = arch_string.split("-")
    arch[1] = os_string
    arch = "-".join(arch)
    return arch


def create_specs(package_name, found_versions, external, cspec, variant):
    """ Construct spec strings from the arguments provided. We first
    find compilers present in compilers.yaml and then create a spec string
    from the compiler specs found. If a variant was provided we add to that
                arch_string = "arch={0}-{1}-{2}".format(
    to the string. We also add the architecture to the string """
    package_specs = {}
    compiler_spec = []
    arch = spack.architecture.sys_type() # Get default arch
    for comp in cspec: # Find all available compiler specs
        compiler_spec.extend(spack.compilers.find(comp.strip("%"))) 
    for ver in found_versions:
        for comp in compiler_spec:
            if "cray" in arch: # If cray in arch, replace with correct os
                arch = replace_os_in_arch_string(arch, comp)
            spec_string = "{0}@{1}%{2}{3} arch={4}".format(
                    package_name, ver, comp, variant if variant else "",
                    arch)
            package_specs[spec_string] = external
    return package_specs    


def create_yaml_dict(package_info, versions):
    """ 
    Packages.yaml entries look like the following: 
        {package_name: 
            buildable : False|True,
            modules|paths:
                spec : module_name | path}

        We first create the specs and then we merge into a dict containing
        the external type (modules|paths) and set buildable to False.
    """            
    # Unload all the relevant information from our pkg info container
    external_name = get_external_name(package_info)
    package_name = get_package_name(package_info)
    external_type = get_external_type(package_info)
    compiler_specs = get_compiler_specs(package_info)
    variant = get_variant_spec(package_info)

    spec_entries = create_specs(package_name, 
                                versions, 
                                external_name, 
                                compiler_specs,
                                variant)

    # Finish off by adding "header"
    package_dict = {"buildable" : False, external_type : spec_entries,
                    "versions" : versions}
    return package_dict


def get_package_entry(packages, package_name):
    return packages.get(package_name, {})


def get_packages_yaml_config(scope=None):
    return spack.config.get_config("packages", scope=scope)


def get_external_specs(package, external_type):
    """ Return specs dict from our package yaml entry """
    return package.get(external_type, {})


def get_specs_from_yaml(packages_yaml, package_name, external_type):
    """ If present, it will return the specs from a given package. If
        not it will just return an empty dict """
    return packages_yaml.get(package_name, {}).get(external_type, {})


def filter_duplicate_specs(package_specs, yaml_specs):
    """ Helper for filtering out duplicate specs """
    return {k : v for k, v in package_specs.items() 
            if k not in yaml_specs.keys()}

def filter_duplicate_versions(old_versions, new_versions)
    return [v for v in new_versions if v not in old_versions]

def add_to_packages_yaml(package_yaml, package_info, scope):
    """ Adds to packages.yaml config file. We first check for any duplicate
        entries. If there are duplicate entries we filter them out. If there
        are no duplicate entries, or there is no entry for a given package
        we simply just add the package to packages.yaml
    """
    package_name = get_package_name(package_info) 
    external_type = get_external_type(package_info) # either modules or paths
    packages = get_packages_yaml_config(scope)
    
    # Find specs for a given package
    specs_from_yaml = get_specs_from_yaml(packages, package_name, external_type)
    # Get specs from our new entry
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
    """ Helper to find out what type of external package we are looking for"""
    if args.modules:
        return "modules"
    else:
        return "paths"


def remove_spec_entry(specs_dict, spec):
    return {k : v for k, v in specs_dict.items() 
            if not Spec(k).satisfies(spec)}


def external_rm(args):
    """ Remove a spec entry from the configuration file. Description of how
    the command works provided above in setup_parser. We compare existing 
    entries. If we find our spec using spec.satisfies, we delete the entry
    """

    external_type = get_external_type_from_args(args)
    packages_yaml = get_packages_yaml_config(args.scope)
    package_spec = Spec(args.external_spec)
    package_name = package_spec.name
    external_package = get_package_entry(packages_yaml, package_name)
    
    if not external_package:
        tty.die("No external_packages match spec %s" % package_spec)
    elif args.all: # delete the entire section
        del packages_yaml[package_name][external_type] 
        spack.config.update_config("packages", packages_yaml, 
                                   scope=args.scope)
    else: 
        specs_dict = get_external_specs(external_package, external_type)
        if specs_dict:
            filtered_config = remove_spec_entry(specs_dict, package_spec)
            if len(filtered_config.keys()) == len(specs_dict.keys()):
                raise PackageSpecInsufficientlySpecificError(package_spec)

            packages_yaml[package_name][external_type] = filtered_config
            spack.config.update_config("packages", 
                                       packages_yaml, 
                                       scope=args.scope)
            tty.msg("Removed package spec %s" % package_spec)


def external(parser, args):
    action = {"add": external_add,
              "rm" : external_rm }
    action[args.external_command](args)


class PackageSpecInsufficientlySpecificError(spack.error.SpackError):
    def __init__(self, package_spec):
        super(PackageSpecInsufficientlySpecificError, self).__init__(
                "Multiple external packages satisfy spec %s" % package_spec)
