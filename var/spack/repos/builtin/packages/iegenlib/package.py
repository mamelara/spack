# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Iegenlib(AutotoolsPackage):
    """Inspector/Executor Generation Library for manipulating sets
       and relations with uninterpreted function symbols. """

    homepage = "http://github.com/CompOpt4Apps/IEGenLib"
    git      = "https://github.com/CompOpt4Apps/IEGenLib.git"
    url      = "https://github.com/CompOpt4Apps/IEGenLib/archive/fc479ee6ff01dba26beffc1dc6bacdba03262138.zip"

    maintainers = ['dhuth']

    version('master', branch='master')
    version('2018-07-03',
        url="https://github.com/CompOpt4Apps/IEGenLib/archive/fc479ee6ff01dba26beffc1dc6bacdba03262138.zip",
        sha256='b4c0b368363fcc1e34b388057cc0940bb87fc336cebb0772fd6055f45009b12b')

    depends_on('cmake@2.6:', type='build')
    depends_on('isl')
    depends_on('texinfo', type='build')
