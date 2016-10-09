from tempfile import mkdtemp
from llnl.util.filesystem import set_executable, mkdirp
import spack.spec
from spack.test.mock_packages_test import *
from spack.external_package import ExternalPackage
from spack.version import Version

common_test_version = "1.10.11"
package_name_with_version_test = "external package 1.10.11"
package_name_with_hypen = "externalpackage-1.10.11"
package_w_ambiguous_output = "v0.06"

test_versions = [common_test_version,
                 package_name_with_version_test,
                 package_name_with_hypen]


def make_mock_external_package(version_output):
    """ Make a directory containing a fake external package. """
    mock_external_dir = mkdtemp()
    external_dir = os.path.join(mock_external_dir, 'external_package')
    share_path = os.path.join(external_dir, "share")
    include_path = os.path.join(external_dir, "include")
    bin_path = os.path.join(external_dir, "bin")

    mkdirp(bin_path)
    mkdirp(share_path)
    mkdirp(include_path)

    external_exe = os.path.join(bin_path, "externalpackage")
    command_help = "externalpackage\nUsage: [-adsf] [-h]"

    with open(external_exe, "w") as f:
        f.write("""\
#!/bin/sh0

for arg in "$@"; do
    if [ "$arg" = -v ] || [ "$arg" = --version ]; then
        echo '%s'
    else
        echo '%s'
    fi
done
""" % (version_output, command_help))

    set_executable(external_exe)
    return mock_external_dir


def removetree(path):
    shutil.rmtree(path, ignore_errors=True)


class TestExternalPackage(MockPackagesTest):
    """ Test external package object """

    def test_package_gets_correct_bin_path(self):
        external_prefix = make_mock_external_package(common_test_version)
        spec = spack.spec.Spec("externalpackage%gcc@4.3")
        try:
            external_package = ExternalPackage(spec,
                                               prefix=external_prefix)
            expected_bin_path = os.path.join(external_prefix,
                                             "external_package",
                                             "bin")
            actual_bin_path = external_package.binary_path()
            self.assertEqual(expected_bin_path, actual_bin_path)
        finally:
            removetree(external_prefix)

    def test_different_version_output_cases(self):
        version_found = []
        # Can find version but if we use incorrect arg return unknown
        expected_versions = "1.10.11"
        spec = spack.spec.Spec("externalpackage%gcc@4.3")
        for test_version in test_versions:
            try:
                external_prefix = make_mock_external_package(test_version)
                external_package = ExternalPackage(spec, prefix=external_prefix)
                actual_version = external_package.version()
                version_found.append((actual_version == expected_versions))
            finally:
                removetree(external_prefix) 
        self.assertTrue(all(version_found))
