import os
from tempfile import mkdtemp
from llnl.util.filesystem import mkdirp, join_path
import spack
import spack.spec
from spack.environment import EnvironmentModifications
from spack.test.mock_packages_test import *
from spack.external_package import ExternalPackage
from spack.version import Version


def set_to_modulepath(path):
    env = EnvironmentModifications()
    env.append_path("MODULEPATH", path)
    env.apply_modifications()
    

def remove_from_modulepath(path):
    env = EnvironmentModifications()
    env.remove_path("MODULEPATH", path)
    env.apply_modifications()


class TestExternalPackage(MockPackagesTest):
    """ Test external package object """

    def setUp(self):
        set_to_modulepath(spack.mock_modulefiles_path)
        super(TestExternalPackage, self).setUp()

    def tearDown(self):
        remove_from_modulepath(spack.mock_modulefiles_path)
        super(TestExternalPackage, self).tearDown()

    def test_package_detection_in_paths(self):
        spec = spack.spec.Spec("externalpackage@1.8.5%gcc@6.1.0")
        found_package = ExternalPackage.detect_package(
                                spec, self.external_package_path)
        expected_package = ExternalPackage(spec, 
                                           self.external_package_path,
                                           "paths")
        self.assertEquals(found_package, expected_package) 

    def test_when_no_package_detected(self):
        spec = spack.spec.Spec("externalpackage@1.8.5%gcc@6.1.0")
        path = "/path/to/externaltool"
        self.assertRaises(SystemExit, ExternalPackage.detect_package, spec, path)
                                                        
    def test_when_no_version_in_spec_and_no_version_detected(self):
        spec = spack.spec.Spec("externalmodule%gcc@4.3")
        module = "externalmodule"
        self.assertRaises(SystemExit, ExternalPackage.detect_package, 
                          spec, module)
    
    def test_package_detection_in_modules(self):
       spec = spack.spec.Spec("externalmodule@1.0%gcc@6.1.0")
       module_name = "externalmodule"
       set_to_modulepath(spack.mock_modulefiles_path)
       found_package = ExternalPackage.detect_package(spec, module_name)
       expected_package = ExternalPackage(spec, module_name, "modules")
       self.assertEquals(found_package, expected_package)
