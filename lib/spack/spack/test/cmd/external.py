import re
from spack.test.mock_packages_test import *
from spack.build_environment import create_module_cmd
from spack.spec import Spec
from spack.util import spack_yaml 
import spack.config
import spack.cmd.external

class MockArgs(object):
    def __init__(self, package_name, path, module, cspec=[]):
        self.package_name = package_name
        self.path = path
        self.module = module
        self.cspec = cspec

class ExternalCmdTest(MockPackagesTest):
    """ Test the external creation of a external spec and also test
    that it gets properly written to a packages.yaml """

    def test_grep_external_from_module_name(self):
        """Given a module arg create a list of versions and package name"""
        mock_args = MockArgs("hdf5", "", "cray-hdf5", ["%gcc", "%clang"])
        if spack.architecture.sys_type() == "cray":
            matches = ['cray-hdf5', ['1.10.0','1.8.14','1.8.16']]
            self.assertEqual(matches, 
                            spack.cmd.external.get_versions_from_args(
                                                                    mock_args))
        else:
            return True

    def test_grep_from_path_given(self):
        """Given a path arg create a lists of versions and package name"""
        mock_args = MockArgs("hdf5", self.opt_path_external, 
                             "", ["%gcc", "%clang"])
        # Need to have fake paths for these packages for the test to work.
        matches = ["hdf5", ["2.0.0", "1.8.16", "1.9.2"]]
        self.assertEqual(matches, 
                         spack.cmd.external.get_versions_from_args(mock_args))


    def test_yaml_dict_creation(self):
        package_specs = {}  # specs created manually
        cspec = ["%gcc", "%clang"]
        test_spec_gcc = "hdf5@1.8.1%gcc" 
        test_spec_clang = "hdf5@1.8.1%clang"
        package_specs[test_spec_gcc] = "cray-hdf5"
        package_specs[test_spec_clang] = "cray-hdf5"

        specs = spack.cmd.external._create_yaml_dict("hdf5", "1.8.1", cspec,
                                                     "cray-hdf5") 
        
        self.assertEqual(package_specs.keys(), specs.keys())


    def test_append_to_yaml(self):
        """ Test that the dicts we created from packages can be written
            to packages.yaml
        """
        old_yaml_dict = spack.config.get_config("packages") 
        cspec = ["%gcc", "%clang"]

        yaml_entry = spack.cmd.external._create_yaml_dict("hdf5",
                                                          "1.8.1", cspec,
                                                          "cray-hdf5") 

        yaml_entry = spack.cmd.external._create_json_entry("hdf5", yaml_entry, 
                                                           "modules")

        spack.config.update_config("packages", yaml_entry) 

        new_yaml_dict = spack.config.get_config("packages")
        
        self.assertNotEquals(old_yaml_dict, new_yaml_dict)
        self.assertTrue("hdf5" in new_yaml_dict.keys())
