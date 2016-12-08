import spack.architecture
import spack.test.mock_packages_test as mock_test
import spack.cmd.external
import spack.config
import spack.spec
import spack.external_package


class MockArgs(object):
    def __init__(self, package_spec="", external_location="", _all=False):
        self.package_spec = package_spec
        self.external_location = external_location
        self.scope = "site"  # Hardcoded for consistency in using site scope
        self.all = _all


def get_packages_config_file():
    return spack.config.get_config("packages", "site")


def get_specs_section(packages_config, name_of_package, external_type):
    return packages_config.get(name_of_package, {}).get(external_type, {})


# Create different types of packages
def create_duplicate_package():
    spec = "externaltool@1.0%gcc@4.5.0"
    return spack.external_package.ExternalPackage(spec, False, "paths",
                                                  "path/to/external_tool")


def create_new_external_package_to_add():
    spec = "externallibrary@1.9.5%gcc@6.1.0"
    return spack.external_package.ExternalPackage(spec, False, "paths",
                                                  "path/to/externallibrary")


def create_external_package_to_add_to_existing_package():
    spec = "externaltool@1.5%gcc@4.5.0"
    path_to_externaltool = "path/to/externaltool_ver1.5"
    return spack.external_package.ExternalPackage(spec, False, "paths",
                                                  path_to_externaltool)


class ExternalCmdTest(mock_test.MockPackagesTest):
    """ Test the external creation of a external spec and also test
    that it gets properly written to a packages.yaml
    """
    #########################
    # test spack external add
    #########################

    def test_append_new_entry_to_config(self):
        external_library = create_new_external_package_to_add()
        spack.external_package.add_external_package(external_library, "site")
        full_packages_config = get_packages_config_file()
        self.assertTrue("externallibrary" in full_packages_config.keys())

        # Check whether the added entry has an appropriate structure
        specs_section = get_specs_section(full_packages_config,
                                          external_library.name,
                                          "paths")
        self.assertTrue("externallibrary@1.9.5%gcc@6.1.0" in
                        specs_section.keys())
        self.assertTrue("path/to/externallibrary" in specs_section.values())

    def test_append_to_existing_entry(self):
        external_tool = create_external_package_to_add_to_existing_package()
        spack.external_package.add_external_package(external_tool, "site")
        full_packages_config = get_packages_config_file()
        self.assertTrue(1 == full_packages_config.keys().count("externaltool"))

        specs_section = get_specs_section(full_packages_config,
                                          external_tool.name,
                                          "paths")
        self.assertTrue(str(external_tool.spec) in specs_section.keys())
        # Test that we didn't overwrite the entire entry with our new one
        self.assertTrue(len(specs_section.keys()) > 1)

    def test_avoid_duplicate_to_existing_entry(self):
        external_tool = create_duplicate_package()
        spack.external_package.add_external_package(external_tool, "site")
        full_packages_config = get_packages_config_file()
        externaltool_specs = get_specs_section(full_packages_config,
                                               external_tool.name,
                                               "paths")

        self.assertTrue(externaltool_specs.keys().count(
            "externaltool@1.0%gcc@4.5.0") == 1)

    ########################
    # test spack external rm
    ########################
    def test_remove_correct_entry_from_config(self):
        spec = spack.spec.Spec("externalmodule@1.0%gcc@4.5.0")
        args = MockArgs(spec)
        spack.cmd.external.external_rm(args)
        full_packages_config = get_packages_config_file()
        external_module_specs = get_specs_section(full_packages_config,
                                                  spec.name,
                                                  "modules")
        self.assertTrue("externalmodule@1.0%gcc@4.5.0"
                        not in external_module_specs.keys())

    def test_error_thrown_when_spec_not_specific(self):
        spec = spack.spec.Spec("externalvirtual")
        args = MockArgs(spec)
        with self.assertRaises(SystemExit):  # tty.error multiple pkg match
            spack.cmd.external.external_rm(args)

    def test_remove_entire_entry_after_specs_section_is_empty(self):
        spec = spack.spec.Spec("externaltool@1.0%gcc@4.5.0")
        args = MockArgs(spec)
        spack.cmd.external.external_rm(args)
        full_packages_config = get_packages_config_file()
        self.assertTrue("externaltool" not in full_packages_config.keys())
        self.assertTrue("externalvirtual" in full_packages_config.keys())

    def test_remove_when_spec_is_not_found(self):
        spec = spack.spec.Spec("boost%gcc@6.1.0")
        args = MockArgs(spec)
        # tty.die(Could not find package for spec..)
        with self.assertRaises(SystemExit): 
            spack.cmd.external.external_rm(args)
