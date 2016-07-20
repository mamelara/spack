from spack.spec import Spec
import spack.cmd.external

test_version = '4.5-spacktest'

class MockArgs(object):
    def __init__(self, path=''):
        self.path = path


class ExternalCmdTest(MockPackagesTest):
    """ Test the external creation of a external spec and also test
    that it gets properly written to a packages.yaml """

    def test_external_spec_creation_properly(self):
        args = MockArgs('externalmodule')
        spack.cmd.external

