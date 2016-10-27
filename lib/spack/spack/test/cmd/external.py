import argparse
import spack.architecture
from spack.test.mock_packages_test import *
from spack.spec import Spec
import spack.config
import spack.cmd
import spack.cmd.external as external
from spack.external_package import ExternalPackage

class MockArgs(object):
    """ Mock arguments that could be passed via the command line """
    def __init__(self, **kwargs): # Use kwargs to generalize for both add & rm
        attrs = ["package_spec", "external_location"]
        for attr in attrs:
            setattr(self, attr, None)

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        self.scope = "site" # Hard code to use 'user' configs
        

class ExternalCmdTest(MockPackagesTest):
    """ Test the external creation of a external spec and also test
    that it gets properly written to a packages.yaml """

    def test_user_path_input_appends_to_packages_config(self):
        args = MockArgs(package_spec="externalpackage@1.8.5%gcc@4.3",
                        external_location=self.external_package_path)
        old_packages_config = spack.config.get_config("packages", 
                                                      scope=args.scope)
        external.external_add(args) 
        updated_packages_config = spack.config.get_config("packages",
                                                          scope=args.scope)

        self.assertTrue("externalpackage" in updated_packages_config)

        externalpackage = updated_packages_config["externalpackage"]

        self.assertTrue(externalpackage["paths"] == 
                {"externalpackage@1.8.5%gcc@4.3": self.external_package_path})

    def test_avoid_duplicate_entries_to_package_yaml(self):
        spec = spack.spec.Spec("externaltool@1.0%gcc@4.5.0")
        external_package = ExternalPackage(spec,
                                           "/path/to/external_tool",
                                           "paths")

        old_packages_config = spack.config.get_config("packages", scope="site")
        external.add_to_packages_yaml(external_package, scope="site")
        packages_config = spack.config.get_config("packages", scope="site")
        externaltool_config = packages_config["externaltool"]["paths"]
        self.assertTrue(externaltool_config.keys().count(
                            "externalpackage@1.0%gcc@4.5.0") < 2)

    def test_user_module_input_appends_to_packages_config(self):
        pass

