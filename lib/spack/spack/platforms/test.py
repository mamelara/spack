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
from spack.architecture import Platform, Target
from spack.architecture import OperatingSystem as OS


class Test(Platform):
    priority    = 1000000
    front_end   = 'x86_32'
    back_end    = 'x86_64'
    default     = 'x86_64'

    front_os = 'redhat6'
    back_os = 'debian6'
    default_os = 'debian6'

    def __init__(self):
        super(Test, self).__init__('test')

        default_target = Target(self.default, "/path/to/backend/modulefile")
        front_end_target = Target(self.front_end,
                                  "/path/to/frontend/modulefile")

        self.add_target(self.default, default_target)
        self.add_target(self.front_end, front_end_target)

        self.add_operating_system(self.default_os, OS('debian', 6))
        self.add_operating_system(self.front_os, OS('redhat', 6))

    @classmethod
    def detect(self):
        return True

    def setup_frontend_environment(self, env):
        env.set('CC', 'test_compiler')
        env.apply_modifications()
