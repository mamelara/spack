import argparse
from spack.test.mock_packages_test import *
from spack.spec import Spec
import spack.config
import spack.cmd
import spack.cmd.external as external

class MockArgs(object):
    """ Mock arguments that could be passed via the command line """
    def __init__(self, **kwargs): # Use kwargs to generalize for both add & rm
        attrs = ["path", "module", "package_name", 
                 "cspecs", "external_spec", "_all",
                 "paths", "modules"]
        # Initialize all attrs with None
        for attr in attrs:
            setattr(self, attr, None)

        # Fill in any provided attributes with the provided keywords args
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        # Hacky way of setting all attribute since all is a reserved keyword
        self.all = False if not self._all else True
        self.scope = "site" # Hard code to use 'user' configs
        

class ExternalCmdTest(MockPackagesTest):
    """ Test the external creation of a external spec and also test
    that it gets properly written to a packages.yaml """

    #def test_external_command_operations(self):
    #    parser = argparse.ArgumentParser()
    #    external.setup_parser(parser)
    #    args1 = parser.parse_args(['add', '-m', 'cray-hdf5', 'gcc', 'clang'])
    #    args2 = parser.parse_args(['add', '-p', '/path/to/hdf5', 'intel', 'gcc']) 
    #    self.assertRaises(ValueError, external.external, parser, args1)
    #    self.assertRaises(ValueError, external.external, parser, args2)

####### Test external add command #########################################
    def test_detect_various_types_of_paths(self):
        """Given a path correctly detect the version from path.
        Tests different formats
        opt_path_package1 is opt/openmpi-1.4.3
        opt_path_package2 is opt/openmpi/1.4.3
        opt_path_package3 is opt/openmpi-1.4.3-6asg2easdar3 (mimics spack)
        """
        package_name = "openmpi" 
        mock_args1 = MockArgs(path=self.opt_path_package1,  
                              package_name=package_name, 
                              cspecs=["gcc", "clang"])

        mock_args2 = MockArgs(path=self.opt_path_package2,  
                              package_name=package_name, 
                              cspecs=["gcc", "clang"])

        mock_args3 = MockArgs(path=self.opt_path_package3,  
                              package_name=package_name, 
                              cspecs=["gcc", "clang"])

        ver1 = external.find_versions_from_args(mock_args1)
        ver2 = external.find_versions_from_args(mock_args2)
        ver3 = external.find_versions_from_args(mock_args3)

        # Check that what we are comparing aren't empty lists
        self.assertTrue(ver1 != [] and ver2 != [] and ver3 != [])

        ver1.sort()
        ver2.sort()
        ver3.sort()
        self.assertTrue(ver1 == ver2 and ver2 == ver3)

    def test_find_versions_from_module_name(self):
        """Given a module arg create a list of versions and package name"""
        mock_args = MockArgs(module="cray-hdf5", 
                             package_name="hdf5", 
                             cspecs=["gcc", "clang"])

        if spack.architecture.sys_type() == "cray":
            expected = {'cray-hdf5', ['1.10.0','1.8.14','1.8.16']}
            expected['cray-hdf5'].sort()
            actual = external.find_versions_from_args(mock_args)
            actual['cray-hdf5'].sort()
            self.assertEqual(expected, actual)
        else:
            return True

    def test_find_versions_from_path_given(self):
        """Given a path arg create a lists of versions and package name"""
        mock_args = MockArgs(path=self.opt_path_external, 
                             package_name="hdf5", 
                             cspecs=["gcc", "clang"])
        # Need to have fake paths for these packages for the test to work.
        expected = ["2.0.0", "1.8.16", "1.9.2"]
        expected.sort()
        actual = external.find_versions_from_args(mock_args)
        actual.sort()
        self.assertEqual(expected, actual)


    def test_yaml_dict_creation(self):
        args = MockArgs(module="cray-hdf5",
                        package_name = "hdf5",
                        cspecs= ["%gcc@4.5.0", "%clang@3.3"])

        expected =  {"buildable": False, 
                         "modules": 
                            {"hdf5@1.8.1%gcc@4.5.0": "cray-hdf5",
                             "hdf5@1.8.1%clang@3.3": "cray-hdf5" }
                    }
        
        package_info = external.collect_package_info(args,"cray-hdf5", 
                                                     "modules")
        found_versions = ["1.8.1"]

        actual_yaml = external.create_yaml_dict(package_info, 
                                                found_versions)  

        
        # Test structure of the dictionary
        self.assertEqual(expected.keys(), actual_yaml.keys())
        self.assertEqual(expected["buildable"],
                         actual_yaml["buildable"])
        self.assertEqual(expected["modules"].keys(),
                         actual_yaml["modules"].keys())



    def test_add_completely_new_entries_to_yaml(self):
        """ Test that the dicts we created from packages can be written
            to packages.yaml
        """
        args = MockArgs(module="cray-hdf5", 
                        package_name="hdf5", 
                        cspecs=["%gcc@4.5.0", "%clang@3.3"])

        external_name = args.module

        package_info = external.collect_package_info(args,
                                                     external_name,
                                                     "modules")
        old_yaml = spack.config.get_config("packages",
                                           scope=args.scope) 
        yaml_entry = external.create_yaml_dict(package_info,
                                               ["1.8.1"])
        external.add_to_packages_yaml(yaml_entry, package_info, args.scope)
        new_yaml = spack.config.get_config("packages", scope=args.scope)  
        self.assertNotEquals(old_yaml, new_yaml)
        self.assertTrue("hdf5" in new_yaml.keys())

    def test_avoid_adding_duplicates_to_yaml(self):
        """ Test that when we add to the yaml file, we don't add duplicates.
        """
        external_name = "externalmodule"

        args = MockArgs(module=external_name,  
                        package_name="externalmodule", 
                        cspecs=["%gcc@4.5.0"])

        package_info = external.collect_package_info(args, "externalmodule",
                                                     "modules")
        versions = ["1.0"]
        
        yaml_entry = external.create_yaml_dict(package_info, versions)
        external.add_to_packages_yaml(yaml_entry, package_info, args.scope)
        packages = spack.config.get_config("packages", scope=args.scope)

        # Test we don't add a duplicate entry
        self.assertTrue(packages.keys().count("externalmodule") < 2)

        actual_specs_dict =  packages["externalmodule"]["modules"]
        expected_specs_dict = ["externalmodule@1.0%gcc@4.5.0",
                               "externalmodule@1.0%clang@3.3"]

        # Test that when we add, we don't accidentally overwrite  
        self.assertEqual(actual_specs_dict.keys(), expected_specs_dict)

    def test_append_new_entries_to_existing_yaml(self):
        """ Test whether we can add new versions without overwriting or
            adding duplicate entries. """

        externaltool_path = "/path/to/external_tool"
        args = MockArgs(path=externaltool_path, 
                        package_name="externaltool", 
                        cspecs=["%gcc@5.3.0", "%clang@3.3", "%gcc@4.5.0"])

        package_info = external.collect_package_info(args, "externaltool", "paths")
        versions = ["1.0"]
        
        yaml_entry = external.create_yaml_dict(package_info, versions)
        external.add_to_packages_yaml(yaml_entry, package_info, args.scope)

        packages = spack.config.get_config("packages", scope=args.scope)

        actual_specs = packages["externaltool"]["paths"].keys()

        expected_specs = ["externaltool@1.0%gcc@4.5.0",
                          "externaltool@1.0%clang@3.3",
                          "externaltool@1.0%gcc@5.3.0"]

        actual_specs.sort()
        expected_specs.sort()
        self.assertEqual(expected_specs, actual_specs)


####### Test external rm command ###################################
    def test_remove_spec_from_yaml(self):
        """ Given a package_name/spec/something else remove from the
            yaml
        """
        spec_string = "externaltool@1.0%gcc@4.5.0"
        spec = Spec(spec_string)
        args = MockArgs(external_spec=spec, _all=False, paths=True)

        old_packages_yaml = spack.config.get_config("packages")
        externaltool_yaml = old_packages_yaml[spec.name]

        external.external_rm(args)

        updated_packages = spack.config.get_config("packages", scope=args.scope)
        updated_externaltool_package = updated_packages[spec.name]

        old_specs = externaltool_yaml["paths"]
        updated_specs = updated_externaltool_package["paths"]

        self.assertTrue(len(old_specs.keys()) != len(updated_specs.keys()))
    
    def test_give_options_to_remove_multiple_entries(self):
        """ Given a spec that has mulitple matches, give the option to delete
            multiple entries 
        """ 
        pass
        #spec_string = "externalmodule@1.0%gcc"
        #spec = Spec(spec_string)
        #args = MockArgs(external_spec=spec, _all=False, modules=True)
        #
        #external.external_rm(args)
        #return

