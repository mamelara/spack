from spack import *

class Craylibsci(Package):
    """The Cray Scientific Libraries package, LibSci, is a collection of
    numerical routines optimized for best performance on Cray systems"""

    homepage = "http://www.nersc.gov/users/software/programming-libraries/math-libraries/libsci"
    url      = "http://www.nersc.gov/users/software/programming-libraries/math-libraries/libsci"

    version("system")

    provides("blas", when="platform=cray")
    provides("lapack", when="platform=cray")
    provides("scalapack", when="platform=cray")

    @property
    def blas_libs(self):
        """Return the location for blas libs"""
        return self.prefix.lib

    @property
    def lapack_libs(self):
        """Return the location for lapack libs"""
        return self.blas_libs

    def install(self, spec, prefix):
        """Throw error when attempting to build package """
        raise UnBuildablePackageError(self)
