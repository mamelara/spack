import argparse
import spack.architecture
from spack.test.mock_packages_test import *
from spack.spec import Spec
from llnl.util.filesystem import mkdirp, join_path, touchp, touch
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


def make_fake_install_path(path, exe_name):
    temp_path = tempfile.mkdtemp()
    fake_root_path = join_path(temp_path, path)
    exe_path = join_path(fake_root_path, "bin", exe_name)
    touchp(exe_path)
    for p in ["lib", "share", "include"]:
        package_path = join_path(fake_root_path, p)
        mkdirp(package_path)
    return fake_root_path 
        

def remove_install_path(path):
    shutil.rmtree(path, ignore_errors=True)


class ExternalCmdTest(MockPackagesTest):
    """ Test the external creation of a external spec and also test
    that it gets properly written to a packages.yaml """

    def test_user_path_input_appends_to_packages_config(self):
        path = "opt/external_package/1.8.5"
        external_package_path = make_fake_install_path(path, "externalpackage")
        args = MockArgs(package_spec="externalpackage@1.8.5%gcc@4.3",
                        external_location=external_package_path)

        old_packages_config = spack.config.get_config("packages", 
                                                      scope=args.scope)
        external.external_add(args) 
        updated_packages_config = spack.config.get_config("packages",
                                                          scope=args.scope)
        remove_install_path(path)

        self.assertTrue("externalpackage" in updated_packages_config)
        externalpackage = updated_packages_config["externalpackage"]
        self.assertTrue(externalpackage["paths"] == 
                {"externalpackage@1.8.5%gcc@4.3": external_package_path})

    def test_avoid_duplicate_entries_to_package_yaml(self):
        spec = spack.spec.Spec("externaltool@1.0%gcc@4.5.0")
        external_package = ExternalPackage(spec,
                                           "/path/to/external_tool",
                                           "paths")

        old_packages_config = spack.config.get_config("packages", scope="site")
        external.add_to_packages_yaml(external_package, scope="site")
        updated_packages_config = spack.config.get_config("packages", 
                                                          scope="site")

        externaltool_config = updated_packages_config["externaltool"]["paths"]
        self.assertTrue(externaltool_config.keys().count(
                            "externalpackage@1.0%gcc@4.5.0") < 2)

    def test_appending_to_an_existing_entry(self):
        path = "path/to/external_tool"
        external_package = make_fake_install_path(path, "externaltool")
        args = MockArgs(package_spec="externaltool@2.0%gcc@4.5.0",
                        external_location=external_package)
        old_packages_config = spack.config.get_config("packages", 
                                                      scope=args.scope)
        external.external_add(args)

        updated_packages_config = spack.config.get_config("packages",
                                                          scope=args.scope)
        remove_install_path(path)
        self.assertTrue("externaltool" in updated_packages_config)
        externaltool = updated_packages_config["externaltool"]
        self.assertTrue(args.package_spec in externaltool["paths"] and
                        "externaltool@1.0%gcc@4.5.0" in externaltool["paths"])

    def test_remove_entry_from_entry(self):
       args = MockArgs(package_spec="externaltool@1.0%gcc@4.5.0")
       package_config = spack.config.get_config("packages", scope="site")
       external.external_rm(args)
       updated_config = spack.config.get_config("packages", scope="site")
       self.assertTrue("externaltool" not in updated_config.keys() and
                        updated_config != {}) 

       args = MockArgs(package_spec="externalmodule@1.0%gcc@4.5.0")
       external.external_rm(args)
       updated_config = spack.config.get_config("packages", scope="site")
       externalmodule = updated_config["externalmodule"]
       specs = externalmodule["modules"]

       self.assertTrue("externalmodule@1.0%gcc@4.5.0" not in specs.keys())

    def test_handles_non_existent_spec(self):
        args = MockArgs(package_spec="externalmodule@2.0")
        self.assertRaises(SystemExit, external.external_rm, args)

