# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Unzip(MakefilePackage):
    """Unzip is a compression and file packaging/archive utility."""

    homepage = 'http://www.info-zip.org/Zip.html'
    url      = 'http://downloads.sourceforge.net/infozip/unzip60.tar.gz'

    version('6.0', '62b490407489521db863b523a7f86375')

    make_args = ['-f', 'unix/Makefile']

    def url_for_version(self, version):
        return 'http://downloads.sourceforge.net/infozip/unzip{0}.tar.gz'.format(version.joined)

    @property
    def build_targets(self):
        if not self.spec.satisfies("platform=cray target=be"):
            self.make_args.append("generic")
            return self.make_args
        else:
            raise InstallError("""Unzip does not build for the backend
architecture on Cray. If you want to use unzip for the backend it is recommended
that you add unzip to packages.yaml:

packages:
   unzip:
     buildable: false
     paths:
       unzip: /usr """)

    @property
    def install_targets(self):
        if not self.spec.satisfies("platform=cray target=be"):
            return self.make_args + ['prefix={0}'.format(self.prefix), 'install']
