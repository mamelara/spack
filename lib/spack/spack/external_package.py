import os
import re
from llnl.util.filesystem import *
from spack.util.executable import Executable


class ExternalPackage(object):
    """ Object represents an external package. It takes in it's
    constructors a prefix or a module and will return a
    version, if it can find a version. Along with path to
    lib, share, include, and manpath
    """
    _version_args = ["-v", "-V", "--version"]

    def __init__(self, spec, **kwargs):
        self._spec = spec
        self._module = kwargs.get("module", None)
        self._prefix = kwargs.get("prefix", None)
        self._bin_path = self._find_binary_path_in_prefix()
        self._version = self._find_matches_in_prefix()

    def version(self):
        return self._version

    def binary_path(self):
        return self._bin_path

    def _find_binary_path_in_prefix(self):
        # Walk down the tree until we find a bin directory
        for dirpath, dirname, fname in os.walk(self._prefix):
            if "bin" in dirname:
                return join_path(dirpath, "bin")
            elif "bin" in dirpath:
                return dirpath

    def _find_candidate_executables_in(self, bin_path):
        candidate_executables = []
        for exe in os.listdir(bin_path):
            exe_path = join_path(bin_path, exe)
            if self._spec.name in exe:  # If exe has package name
                candidate_executables.append(exe_path)
        return candidate_executables

    def _detect_version(self, regexp, executables):
        for x in executables:
            x = os.path.abspath(x)
            exe = Executable(x)
            for v in self._version_args:
                output = exe(v, output=str, error=str)
                match = re.search(regexp, output)
                if not match:
                    continue
                else:
                    ver = match.group(1)
                    return ver
        return "unknown"

    def _find_matches_in_prefix(self):
        """ Tests for finding executables, We find our binary and then
            we run tests on the output """
        regexp_for_version = r'(?:%s)?[.\-]*(\d.[\d+\.]+)' % self._spec.name
        candidate_executables = self._find_candidate_executables_in(
                                                                self._bin_path)
        version = self._detect_version(regexp_for_version,
                                       candidate_executables)
        return version
