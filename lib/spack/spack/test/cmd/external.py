import re
from spack.test.mock_packages_test import *
from spack.build_environment import create_modulecmd
from spack.spec import Spec
from spack.util import spack_yaml 
import spack.cmd.external

class MockArgs(object):
    def __init__(self, path, module, cspec=[]):
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
        mock_args = MockArgs("", "cray-hdf5")
        modulecmd = create_modulecmd()
        output = modulecmd("avail", mock_args.module, output=str, error=str)
        module_regex = r'({0})/([.\d]+)(\(default\))?'.format(mock_args.module)
        matches = re.findall(module_regex, output)
        self.assertEqual(matches, 
                         spack.cmd.external.grep_for_package_name(mock_args))

    def test_spec_creation(self):
        package_specs = []  # specs created manually
        cspec = ["%gcc", "%clang"]
        test_spec_gcc = Spec("cray-hdf5%gcc") # Probably need to create mock package
        test_spec_clang = Spec("cray-hdf5%clang")
        test_spec_gcc.concretize()
        test_spec_clang.concretize()
        package_specs.append(test_spec_gcc)
        package_specs.append(test_spec_clang)

        specs = spack.cmd.external.create_specs("cray-hdf5", "1.8.1", cspec) 

        self.assertEqual(package_specs, specs)

    def test_create_yaml_dict(self):
        spec_clang = Spec("cray-hdf5@1.8.1%clang")
        spec_gcc = Spec("cray-hdf5@1.8.1%gcc")

        spec_intel.concretize()
        spec_gcc.concretize()

        yaml_entry = {"hdf5" : 
                            { "modules" : 
                                  {spec_clang : "cray-hdf5",
                                   spec_gcc : "cray-hdf5" }}}

        
        

