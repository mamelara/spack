import os
import re

from llnl.util.filesystem import *
from llnl.util.lang import key_ordering
import llnl.util.tty as tty

from spack.build_environment import create_module_cmd, get_path_from_module
from spack.util.executable import *
import spack.spec


def _find_external_type(external_package):
    """ Finds whether the package is a module or a path """
    if os.path.isdir(external_package):
        return "paths"
    else:
        modulecmd = create_module_cmd()
        if modulecmd:
            output = modulecmd("show", external_package, output=str, error=str)
            if "ERROR" not in output:
                return "modules"
        return "unknown"


def _validate_package_path_installation(path, spec):
    """ Determines whether the path or module matches what the user specified
        in the spec """

    def search_package_directory(path, dirname):
        """ search package directory for files that match package name"""
        dirpath = join_path(path, dirname)
        if os.path.exists(dirpath):
            files = os.listdir(dirpath)
            for f in files:
                if spec.name in f:
                    return True

    valid_checks = []  # Check bin, lib and share for package name
    for directory in ["bin", "lib", "share", "include"]:
        valid_checks.append(search_package_directory(path, directory))
    if not any(valid_checks):
        tty.die("Incorrect path: %s for package %s" % (path, spec))


def _detect_version_by_prefix(path):
    """ Some paths will have the version as the parent directory to the
        package. We first check if we can grep a version from there."""
    dirnames = path.split("/")
    for directory in dirnames:
        try:
            num_list = []
            if "-" in directory:  #  some names may have name-version
                dir_list = directory.split("-")
                num_list = dir_list[1]  #  if split we have [name, version]
            num_list = directory.split(".")
            int(num_list[0])
            return directory
        except ValueError:
            continue


def get_pkg_config():
    pkg_config = which("pkg-config")
    return pkg_config


def _detect_version_by_pkgconfig(path):
    pkg_config = get_pkg_config()
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
    checks = [_detect_version_by_prefix,
              _detect_version_by_pkgconfig]
    versions = set()
    for check in checks:
        ver = check(path)
        if ver:
            versions.add(ver)
    if len(versions) == 1:
        return versions.pop()


def _detect_from_module_avail(output):
    """ Find versions in module avail output """
    for line in output:
        if "_VERSION" in line or "_VER" in line:
            line_split = line.split()
            return line_split[2]


def _detect_version_by_module(module_name):
    """ Attempt to detect a version from a module name """
    modulecmd = create_module_cmd()
    output = modulecmd("avail", module_name, output=str, error=str)
    versions = _detect_from_module_avail(output)
    return versions


def _get_version_from_spec(spec):
    try:
        return str(spec.version)
    except spack.spec.SpecError:
        return None


def _detect_version(external_package, ext_type):
    """Attempts to detect version from the location provided"""
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

    @classmethod
    def detect_package(cls, spec, external_location):
        """ Finds and verifies a package.
            Returns package objects that can be used to
            append to packages.yaml """

        external_type = _find_external_type(external_location)
        if external_type == "unknown":
            tty.die("Could not detect correct path or module for %s" % spec)
        elif external_type == "paths":
            # Does further checks to make sure that package exists in dir
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
        if spec_version == found_version:  # If versions match no need to update
            return spec
        elif spec_version and found_version != spec_version:
                raise IncorrectPackageVersionError(
                    "detected version %s  does not match version supplied "
                    " in spec %s" % (found_version, spec_version))
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
