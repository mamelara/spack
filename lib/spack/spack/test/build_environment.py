##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import pytest

import spack.build_environment
from spack.environment import EnvironmentModifications
import spack.spec
from spack.paths import build_env_path
<<<<<<< Updated upstream
from spack.build_environment import (dso_suffix, _static_to_shared_library,
                                     build_env_compilers)
=======
<<<<<<< Updated upstream
from spack.build_environment import dso_suffix, _static_to_shared_library
>>>>>>> Stashed changes
from spack.util.executable import Executable
=======
from spack.build_environment import (dso_suffix, _static_to_shared_library,
                                     build_env_compilers)
from spack.util.executable import Executable, which
>>>>>>> Stashed changes


@pytest.fixture
def build_environment():
    cc = Executable(os.path.join(build_env_path, "cc"))
    cxx = Executable(os.path.join(build_env_path, "c++"))
    fc = Executable(os.path.join(build_env_path, "fc"))

    realcc = "/bin/mycc"
    prefix = "/spack-test-prefix"

    os.environ['SPACK_CC'] = realcc
    os.environ['SPACK_CXX'] = realcc
    os.environ['SPACK_FC'] = realcc

    os.environ['SPACK_PREFIX'] = prefix
    os.environ['SPACK_ENV_PATH'] = "test"
    os.environ['SPACK_DEBUG_LOG_DIR'] = "."
    os.environ['SPACK_DEBUG_LOG_ID'] = "foo-hashabc"
    os.environ['SPACK_COMPILER_SPEC'] = "gcc@4.4.7"
    os.environ['SPACK_SHORT_SPEC'] = (
        "foo@1.2 arch=linux-rhel6-x86_64 /hashabc")

    os.environ['SPACK_CC_RPATH_ARG']  = "-Wl,-rpath,"
    os.environ['SPACK_CXX_RPATH_ARG'] = "-Wl,-rpath,"
    os.environ['SPACK_F77_RPATH_ARG'] = "-Wl,-rpath,"
    os.environ['SPACK_FC_RPATH_ARG']  = "-Wl,-rpath,"

    if 'SPACK_DEPENDENCIES' in os.environ:
        del os.environ['SPACK_DEPENDENCIES']

    yield {'cc': cc, 'cxx': cxx, 'fc': fc}

    for name in ('SPACK_CC', 'SPACK_CXX', 'SPACK_FC', 'SPACK_PREFIX',
                 'SPACK_ENV_PATH', 'SPACK_DEBUG_LOG_DIR',
                 'SPACK_COMPILER_SPEC', 'SPACK_SHORT_SPEC',
                 'SPACK_CC_RPATH_ARG', 'SPACK_CXX_RPATH_ARG',
                 'SPACK_F77_RPATH_ARG', 'SPACK_FC_RPATH_ARG'):
        del os.environ[name]


def test_static_to_shared_library(build_environment):
    os.environ['SPACK_TEST_COMMAND'] = 'dump-args'

    expected = {
        'linux': ('/bin/mycc -Wl,-rpath,/spack-test-prefix/lib'
                  ' -Wl,-rpath,/spack-test-prefix/lib64 -shared'
                  ' -Wl,-soname,{2} -Wl,--whole-archive {0}'
                  ' -Wl,--no-whole-archive -o {1}'),
        'darwin': ('/bin/mycc -Wl,-rpath,/spack-test-prefix/lib'
                   ' -Wl,-rpath,/spack-test-prefix/lib64 -dynamiclib'
                   ' -install_name {1} -Wl,-force_load,{0} -o {1}')
    }

    static_lib = '/spack/libfoo.a'

    for arch in ('linux', 'darwin'):
        for shared_lib in (None, '/spack/libbar.so'):
            output = _static_to_shared_library(arch, build_environment['cc'],
                                               static_lib, shared_lib,
                                               compiler_output=str).strip()

            if not shared_lib:
                shared_lib = '{0}.{1}'.format(
                    os.path.splitext(static_lib)[0], dso_suffix)

            assert output == expected[arch].format(
                static_lib, shared_lib, os.path.basename(shared_lib))


@pytest.mark.regression('8345')
@pytest.mark.usefixtures('config', 'mock_packages')
def test_cc_not_changed_by_modules(monkeypatch):

    s = spack.spec.Spec('cmake')
    s.concretize()
    pkg = s.package

    def _set_wrong_cc(x):
        os.environ['CC'] = 'NOT_THIS_PLEASE'
        os.environ['ANOTHER_VAR'] = 'THIS_IS_SET'

    monkeypatch.setattr(
        spack.build_environment, 'load_module', _set_wrong_cc
    )
    monkeypatch.setattr(
        pkg.compiler, 'modules', ['some_module']
    )

    spack.build_environment.setup_package(pkg, False)

    assert os.environ['CC'] != 'NOT_THIS_PLEASE'
    assert os.environ['ANOTHER_VAR'] == 'THIS_IS_SET'


@pytest.mark.usefixtures('config', 'mock_packages')
def test_cross_compiler_swapped():

    s = spack.spec.Spec("cmake")
    s.concretize()
    pkg = s.package
    env = EnvironmentModifications()

    original_compiler = os.environ['SPACK_CC']

    build_env_context_manager = build_env_compilers(pkg, env)

    with build_env_context_manager():
        swapped_compiler = os.environ['SPACK_CC']

    # test that we swapped
    assert swapped_compiler and original_compiler != swapped_compiler

    # test that we are back to our original
    assert os.environ["SPACK_CC"] == original_compiler


@pytest.mark.usefixtures('config', 'mock_packages')
def test_cross_compiler_swapped(mock_configure):

    s = spack.spec.Spec('mpileaks')
    s.concretize()
    pkg = s.package
    platform = pkg.architecture.platform
    env = EnvironmentModifications()

    os.environ['CC'] = 'back-end-compiler'
    configure = which('configure')
    with_frontend_comp = build_env_compilers(pkg, platform, env)
    configure = with_frontend_comp(configure)
    swapped_compiler = configure('CC', stdout=str)

    assert swapped_compiler and os.environ['CC'] != swapped_compiler
