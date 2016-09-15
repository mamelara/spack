import argparse
from spack.test.mock_packages_test import *
from spack.spec import Spec
import spack.config
import spack.cmd.external as external

class MockArgs(object):
    def __init__(self, package_name, path, module, cspec=[]):
        self.package_name = package_name
        self.path = path
        self.module = module
        self.cspec = cspec

class ExternalCmdTest(MockPackagesTest):
    """ Test the external creation of a external spec and also test
    that it gets properly written to a packages.yaml """

    def test_external_command_operations(self):
        parser = argparse.ArgumentParser()
        external.setup_parser(parser)
        args1 = parser.parse_args(['-m', 'cray-hdf5', '%gcc', '%clang'])
        args2 = parser.parse_args(['-p', '/path/to/hdf5', '%intel', '%gcc']) 
        self.assertRaises(ValueError, external.external, parser, args1)
        self.assertRaises(ValueError, external.external, parser, args2)

    def test_detect_various_types_of_paths(self):
        """Given a path correctly detect the version from path.
           Tests different formats
        opt_path_package1 is opt/openmpi-1.4.3
        opt_path_package2 is opt/openmpi/1.4.3
        opt_path_package3 is opt/openmpi-1.4.3-6asg2easdar3 (mimics spack)
        """
        
        mock_args1 = MockArgs("openmpi", self.opt_path_package1, "", ["%gcc", "%clang"])
        mock_args2 = MockArgs("openmpi", self.opt_path_package2, "", ["%gcc", "%clang"])
        mock_args3 = MockArgs("openmpi", self.opt_path_package3, "", ["%gcc", "%clang"])
        ver1 = external.get_versions_from_args(mock_args1)
        ver2 = external.get_versions_from_args(mock_args2)
        ver3 = external.get_versions_from_args(mock_args3)
        print ver1
        assert(ver1[1] != [])
        assert(ver2[1] != [])
        assert(ver3[1] != [])
        self.assertTrue(ver1 == ver2 and ver2 == ver3)

    def test_grep_external_from_module_name(self):
        """Given a module arg create a list of versions and package name"""
        mock_args = MockArgs("hdf5", "", "cray-hdf5", ["%gcc", "%clang"])
        if spack.architecture.sys_type() == "cray":
            matches = ['cray-hdf5', ['1.10.0','1.8.14','1.8.16']]
            self.assertEqual(matches, 
                             external.get_versions_from_args(mock_args))
        else:
            return True

    def test_grep_from_path_given(self):
        """Given a path arg create a lists of versions and package name"""
        mock_args = MockArgs("hdf5", self.opt_path_external, 
                             "", ["%gcc", "%clang"])
        # Need to have fake paths for these packages for the test to work.
        matches = ["hdf5", ["2.0.0", "1.8.16", "1.9.2"]]
        self.assertEqual(matches, 
                         external.get_versions_from_args(mock_args))


    def test_yaml_dict_creation(self):
        package_specs = {}  # specs created manually
        cspec = ["%gcc", "%clang"]
        test_spec_gcc = "hdf5@1.8.1%gcc" 
        test_spec_clang = "hdf5@1.8.1%clang"
        package_specs[test_spec_gcc] = "cray-hdf5"
        package_specs[test_spec_clang] = "cray-hdf5"
        specs = external._create_yaml_dict("hdf5", "1.8.1", cspec, "cray-hdf5")  
        self.assertEqual(package_specs.keys(), specs.keys())


    def test_append_to_yaml(self):
        """ Test that the dicts we created from packages can be written
            to packages.yaml
        """
        old_yaml_dict = spack.config.get_config("packages") 
        cspec = ["%gcc", "%clang"]

        yaml_entry = external._create_yaml_dict("hdf5", "1.8.1", cspec, 
                                                                 "cray-hdf5") 

        yaml_entry = external._create_json_entry("hdf5", yaml_entry, 
                                                         "modules")

        spack.config.update_config("packages", yaml_entry) 

        new_yaml_dict = spack.config.get_config("packages")
        
        self.assertNotEquals(old_yaml_dict, new_yaml_dict)
        self.assertTrue("hdf5" in new_yaml_dict.keys())
