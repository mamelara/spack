import os
import re

from llnl.util.filesystem import *
from llnl.util.lang import key_ordering
import llnl.util.tty as tty
from spack.build_environment import create_module_cmd, get_path_from_module
from spack.util.spack_yaml import syaml_dict
from spack.util.executable import *
import spack.spec


def _find_external_type(external_package_location):
    """Tests to determine whether the provided package location is
       a path to an installation or a module name. 
       
       returns a string indicating the detected location:
            paths:  given arg is a path to the package installation
            modules: given arg is a module name and responds to modulecmd
            unknown: given arg cannot be detected
    """   
    if os.path.isdir(external_package_location):
        return "paths"
    else:
        modulecmd = create_module_cmd()
        if modulecmd:
            output = modulecmd("show", external_package_location, 
                               output=str, error=str)
            if "ERROR" not in output:
                return "modules"
        return "unknown"


def _validate_package_path_installation(path, spec):
    """ Validates the package install path.

    If true then the package is what the user specified in the spec.
    Returns false when the package install path does not match spec """

    def find_spec_name_match_in_directory(dirpath):
        """ search package directory for files that match package name"""
        if os.path.exists(dirpath):
            files = os.listdir(dirpath)
            for f in files:
                if spec.name in f:
                    return True

    valid_checks = [] 
    for directory in ["bin", "lib", "share", "include"]:
        dirpath = join_path(path, directory)
        valid_checks.append(find_spec_name_match_in_directory(dirpath))
    if not any(valid_checks):
        tty.die("Incorrect path: %s for package %s" % (path, spec))


def _directory_string_represents_version(directory):
    """Tests whether a string matches a version string i.e has a format 
       similar to 1.0.0. 
       Returns true if the directory string represents a version string """
    try:
        num_list = []
        if "-" in directory:
            dir_list = directory.split("-")
            num_list = dir_list[1]
        num_list = directory.split(".")
        int(num_list[0])
        return True
    except ValueError:
        return False


def _detect_version_by_prefix(path):
    """Attempts to find a string that represents a version ie 1.0.0.
       If found it returns the directory, else None """
    dirnames = path.split("/")
    for directory in dirnames:
        if _directory_string_represents_version(directory):
            return directory
        else:
            continue


def _detect_version_by_pkgconfig(path):
    """Attempt to detect the version of a package via pkg-config. 
    
    If there is a valid output, return the output. Else return None """
    def get_pkg_config_exe():
        pkg_config = which("pkg-config")
        return pkg_config

    pkg_config = get_pkg_config_exe()

    regex = r'(^\d+\.[\d\.]*)' 
    try:
        output = pkg_config("--modversion", spec.name, output=str, error=str)
        match = re.search(regex, output)
        return match.group(0) if match else "unknown"
    except ProcessError:
        return None
    except Exception:
        return None


def _detect_version_using_path(path):
    """ Attempts to detect version by either it's prefix or by pkg-config.

        If there are any successful checks, then return the output. 
        Else returns None"""

    checks = [_detect_version_by_prefix,
              _detect_version_by_pkgconfig]

    # refactor this, odd that we add to set only to pop
    versions = set()
    for check in checks:
        ver = check(path)
        if ver:
            versions.add(ver)
    if len(versions) == 1:
        return versions.pop()


def _detect_from_module_avail(output):
    """Attempts to parse the output of modulecmd for a version 
       Returns the version string"""
    for line in output:
        if "_VERSION" in line or "_VER" in line:
            line_split = line.split()
            # Follows pattern  setenv|prepend_path   _VERSION|_VER   <version>
            return line_split[2] 


def _detect_version_by_module(module_name):
    """Uses a module name to parse a version string. 
       If successful, returns that string else returns None """
    modulecmd = create_module_cmd()
    output = modulecmd("avail", module_name, output=str, error=str)
    versions = _detect_from_module_avail(output)
    return versions


def _detect_version(external_package, ext_type):
    """
    Requires that external_package is a valid module or path.
    Detects version either by the package install prefix or by the module
    name.  

    Can return either None or a version if found 
    """

    if ext_type == "paths":
        return _detect_version_using_path(external_package)
    else:
        return _detect_version_by_module(external_package)


@key_ordering
class ExternalPackage(object):
    """ Object represents an external package. It takes in it's
    constructors a prefix or a module and will return a
    version, if it can find a version. """

    def __init__(self, spec, external_package, external_type):
        self._spec = spec
        self._external_package = external_package
        self._external_type = external_type

    @property
    def version(self):
        return self._spec.version

    @property
    def name(self):
        return self._spec.name

    @property
    def external_type(self):
        return self._external_type

    @property
    def external_location(self):
        return self._external_package

    @property
    def spec(self):
        return self._spec

    def _cmp_key(self):
        return (self._spec, self._external_package, self._external_type)

    def __str__(self):
        return str(self._spec)

    def __repr__(self):
        return "ExternalPackage(%s, %s)" % (self._spec, self._external_package)

    def spec_dict(self):
        """ Return the specs section of a package yaml """
        return syaml_dict([(str(self.spec), self.external_location)])

    def to_dict(self):
        """ Return syaml dictionary from object"""
        entry = syaml_dict([("buildable", False), (self.external_type,
                    self.spec_dict())])
        return syaml_dict([(self.name, entry)])


    @classmethod
    def detect_package(cls, spec, external_location):
        """ Detects a package installation by either it's install path or
            it's module name.
            
            Returns an external package object.
        """
        def _get_version_from_spec(spec):
            try:
                return str(spec.version)
            except spack.spec.SpecError:
                return None

        external_type = _find_external_type(external_location)

        if external_type == "unknown":
            tty.die("Could not detect correct path or module for %s" % spec)
        elif external_type == "paths":
            _validate_package_path_installation(external_location, spec)

        found_version = _detect_version(external_location, external_type)
        spec_version = _get_version_from_spec(spec)

        if not found_version and not spec_version:
            tty.die("Could not detect version for package %s\n"
                    "Please provide a spec with a version" % spec)

        package_spec = cls._update_spec(spec, spec_version, found_version)
        external_package = ExternalPackage(package_spec,
                                           external_location,
                                           external_type)
        return external_package

    @classmethod
    def _update_spec(cls, spec, spec_version, found_version):
        if not found_version:
            return spec
        if spec_version:
            assert spec_version == found_version
        spec_string = str(spec)
        index = len(spec.name)  # index where we want to change version
        new_spec_string = spec_string[:index] + \
            "@{0}".format(found_version) + spec_string[index:]
        new_spec = spack.spec.Spec(new_spec_string)
        return new_spec


class ExternalPackageError(spack.error.SpackError):
    """ Raised when a given prefix for an external package is incorrect """
    def __init__(self, message, long_msg=None):
        super(ExternalPackageError, self).__init__(message, long_msg)


class IncorrectPackageVersionError(spack.error.SpackError):
    """ Raised when the package provided at path does not match spec """
    def __init__(self, message, long_msg=None):
        super(IncorrectPackageVersionError, self).__init__(message, long_msg)
