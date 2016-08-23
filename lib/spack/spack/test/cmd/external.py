import re
from spack.test.mock_packages_test import *
from spack.build_environment import create_module_cmd
from spack.spec import Spec
from spack.util import spack_yaml 
import spack.config
import spack.cmd.external

class MockArgs(object):
    def __init__(self, package, path, module, cspec=[]):
        self.path = path
        self.module = module
        self.cspec = cspec

class ExternalCmdTest(MockPackagesTest):
    """ Test the external creation of a external spec and also test
    that it gets properly written to a packages.yaml """

    def test_grep_external_from_module_name(self):
        """ Test case should be our hdf5 module name. It should read
        all the available greps from hdf5 and put them in some kind of
        pair structure where we have the package name and version number
        """
        # Not a robust test since modules all have different names
        mock_args = MockArgs("hdf5", "", "cray-hdf5", ["%gcc", "%clang"])
        if spack.architecture.sys_type() == "cray":
            matches = [('cray-hdf5', '1.10.0'), 
                    ('cray-hdf5', '1.8.14'), 
                    ('cray-hdf5', '1.8.16')]
            self.assertEqual(matches, 
                            spack.cmd.external.grep_for_package_name(
                                                                    mock_args))
        else:
            return True

    def test_grep_from_path_given(self):
        """ Given the path type of arg given, it should be able to detect which
        versions are available and then return a list of tuple pairs """
        mock_args = MockArgs("hdf5", self.opt_path_external, 
                             "", ["%gcc", "%clang"])
        # Need to have fake paths for these packages for the test to work.
        matches = [("hdf5", "2.0.0"), ("hdf5", "1.8.16"), ("hdf5", "1.9.2")]
        self.assertEqual(matches, 
                         spack.cmd.external.grep_for_package_name(mock_args))


    def test_spec_creation(self):
        package_specs = []  # specs created manually
        cspec = ["%gcc", "%clang"]
        test_spec_gcc = Spec("cray-hdf5%gcc") # Probably need to create mock package
        test_spec_clang = Spec("cray-hdf5%clang")
        test_spec_gcc.concretize()
        test_spec_clang.concretize()
        package_specs.append((test_spec_gcc, "cray-hdf5"))
        package_specs.append((test_spec_clang, "cray-hdf5"))

        specs = spack.cmd.external.create_specs("cray-hdf5", "1.8.1", cspec) 
        
        assert len(package_specs) == len(specs)

        for spec, name in zip(specs, package_specs):
            print spec, name

        self.assertEqual(package_specs, specs)

    def test_create_yaml_dict(self):
        list_of_specs = []
        spec_clang = Spec("cray-hdf5@1.8.1%clang")
        spec_gcc = Spec("cray-hdf5@1.8.1%gcc")

        spec_clang.concretize()
        spec_gcc.concretize()
        
        list_of_specs.extend([(spec_clang, "cray-hdf5"), 
                              (spec_gcc, "cray-hdf5")])
        
        yaml_expected = {"hdf5" :    
                            {"buildable": False, 
                             "modules" : 
                             {str(spec_clang) : "cray-hdf5",
                              str(spec_gcc) : "cray-hdf5" }}}

        yaml_actual = spack.cmd.external.create_json_entry("hdf5",
                                                           list_of_specs, True)

        self.assertEqual(yaml_expected, yaml_actual)

    def test_append_to_yaml(self):
        """ Test that the dicts we created from packages can be written
            to packages.yaml
        """
        old_yaml_dict = spack.config.get_config("packages") 
        list_of_specs = []
        spec_clang = Spec("cray-hdf5@1.8.1%clang")
        spec_gcc   = Spec("cray-hdf5@1.8.1%gcc")

        spec_clang.concretize()
        spec_gcc.concretize()

        list_of_specs.extend([(spec_clang, "cray-hdf5"),
                              (spec_gcc, "cray-hdf5")])

        yaml_entry = spack.cmd.external.create_json_entry("hdf5",
                                                           list_of_specs, True) 
        spack.config.update_config("packages", yaml_entry) 
        new_yaml_dict = spack.config.get_config("packages")
        
        self.assertNotEquals(old_yaml_dict, new_yaml_dict)
        self.assertTrue("hdf5" in new_yaml_dict.keys())
