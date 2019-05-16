# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libcircle(AutotoolsPackage):
    """libcircle provides an efficient distributed queue on a cluster,
       using self-stabilizing work stealing."""

    homepage = "https://github.com/hpc/libcircle"

    version('0.2.1-rc.1', '2b1369a5736457239f908abf88143ec2',
            url='https://github.com/hpc/libcircle/releases/download/0.2.1-rc.1/libcircle-0.2.1-rc.1.tar.gz')

    depends_on('mpi')
    depends_on("m4")
    depends_on("libtool")
    depends_on("autoconf")
    depends_on("automake")

    patch_url = "https://github.com/JulianKunkel/libcircle/commit/612ae5537d0c284af7a5d349f3a2428a3f11a99b.patch"
    patch_checksum = "85268ecd5b4ea9eadfedf187d8f689016fcfed53a0d720fca444670d4be596fc"
    #patch_checksum = "16d592a34d062fb9c8047a71ec3bc81312afd646c74ec43621448f5ec3e835d0"

    patch(patch_url, sha256=patch_checksum, when="platform=cray", level=1)

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
