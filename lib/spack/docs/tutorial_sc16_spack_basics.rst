.. _basics-tutorial:

=========================================
Basic Installation Tutorial
=========================================

This tutorial will guide you through the process of installing software
using Spack. We will first cover the `spack install` command, focusing on
the power of the spec syntax and the flexibility it gives to users. We
will also cover the `spack find` command for viewing installed packages
and the `spack uninstall` command. Finally, we will touch on how Spack
manages compilers, especially as it relates to using Spack-built
compilers within Spack. We will include full output from all of the
commands demonstrated, although we will frequently call attention to only
small portions of that output (or merely to the fact that it
succeeded). The provided output is all from a cluster running Red Hat
Enterprise Linux.

IMPORTANT NOTE: For NERSC, we will be running this on Cori. 
In order to avoid clogging up the login nodes it is VERY IMPORTANT that 
you add `-j8` or anything that does not use all 32 cores. Spack can get greedy 
and when you have a bunch of people installing and using `-j32` 
default things can get slow.

.. _basics-tutorial-install:

----------------
Installing Spack
----------------

Spack works out of the box. Simply clone spack and get going.
We will be using a forked branch that I have provided that includes some
configurations that will be useful for compiling on Cori.

.. code-block:: console

  mamelara:~$ git clone https://github.com/mamelara/spack.git
  Cloning into 'spack' ...
  remote: Counting objects: 47125, done.
  remote: Compressing objects: 100% (68/68), done.
  remote: Total 47125 (delta 16), reused 2 (delta 2), pack-reused 47047
  Receiving objects: 100% (47125/47125), 12.02 MiB | 2.11 MiB/s, done.
  Resolving deltas: 100% (23044/23044), done.
  $ cd spack
  mamelara:~$ cd spack
  mamelara:~$ git checkout nersc_tutorial

Then add Spack to your path.

.. code-block:: console

  $ export PATH=~/spack/bin:$PATH

You're good to go!

-----------------
What is in Spack?
-----------------

The ``spack list`` command shows available packages.

.. code-block:: console

  $ spack list
  ==> 1016 packages.
  abinit                           hwloc                  piranha              r-rjava
  ack                              hydra                  pixman               r-rjson
  activeharmony                    hypre                  pkg-config           r-rjsonio
  ...

The ``spack list`` command can also take a query string. Spack
automatically adds wildcards to both ends of the string. For example,
we can view all available python packages.

.. code-block:: console

  $ spack list py
  ==> 129 packages.
  py-3to2            py-epydoc          py-nestle         py-pycparser         py-six
  py-alabaster       py-flake8          py-netcdf         py-pydatalog         py-sncosmo
  py-argcomplete     py-funcsigs        py-networkx       py-pyelftools        py-snowballstemmer
  ...

-------------------
Installing Packages
-------------------

Installing a package with Spack is very simple. To install a piece of
software, simply type ``spack install <package_name>``

As a reminder be sure to add ``-j4`` like so: 
``spack install -j4 <package_name>``

.. code-block:: console
    
    $ spack install -j4 libelf
    ==> Installing libelf
    ==> Using cached archive: /global/u2/m/mamelara/spack/var/spack/cache/libelf/libelf-0.8.13.tar.gz
    ==> Staging archive: /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.13-bkwhzgecutmhfzo2fsaybsya2ldhxgjf/libelf-0.8.13.tar.gz
    ==> Created stage in /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.13-bkwhzgecutmhfzo2fsaybsya2ldhxgjf
    ==> Ran patch() for libelf
    ==> Building libelf [AutotoolsPackage]
    ==> Executing phase : 'autoreconf'
    ==> Executing phase : 'configure'
    ==> Executing phase : 'build'
    ==> Executing phase : 'install'
    ==> Successfully installed libelf
    Fetch: 0.01s.  Build: 22.23s.  Total: 22.24s.
    [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libelf-0.8.13-bkwhzgecutmhfzo2fsaybsya2ldhxgjf

Spack's spec syntax is the interface by which we can request specific
configurations of the package. The ``%`` sigil is used to specify
compilers.

.. code-block:: console

    $ spack install -j4 libelf %intel
    ==> Installing libelf
    ==> Using cached archive: /global/u2/m/mamelara/spack/var/spack/cache/libelf/libelf-0.8.13.tar.gz
    ==> Staging archive: /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.13-ununouuxni5psalrxikvscx4wpagpktd/libelf-0.8.13.tar.gz
    ==> Created stage in /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.13-ununouuxni5psalrxikvscx4wpagpktd
    ==> Ran patch() for libelf
    ==> Building libelf [AutotoolsPackage]
    ==> Executing phase : 'autoreconf'
    ==> Executing phase : 'configure'
    ==> Executing phase : 'build'
    ==> Executing phase : 'install'
    ==> Successfully installed libelf
    Fetch: 0.01s.  Build: 1m 17.12s.  Total: 1m 17.12s.
    [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/intel-17.0.1.132/libelf-0.8.13-ununouuxni5psalrxikvscx4wpagpktd

Note that this installation is located separately from the previous
one. We will discuss this in more detail later, but this is part of what
allows Spack to support arbitrarily versioned software.

You can check for particular versions before requesting them. We will
use the ``spack versions`` command to see the available versions, and then
install a different version of ``libelf``.

.. code-block:: console

  $ spack versions libelf
  ==> Safe versions (already checksummed):
    0.8.13
    0.8.12
  ==> Remote versions (not yet checksummed):
    0.8.11
    0.8.10
    0.8.9
    0.8.8
    0.8.7
    0.8.6
    0.8.5
    0.8.4
    0.8.3
    0.8.2
    0.8.0
    0.7.0
    0.6.4
    0.5.2


The ``@`` sigil is used to specify versions, both of packages and of
compilers.

.. code-block:: console

  $ spack install -j4 libelf @0.8.12
  ==> Installing libelf
  ==> Trying to fetch from ~/spack/var/spack/cache/libelf/libelf-0.8.12.tar.gz
  curl: (37) Couldn't open file ~/spack/var/spack/cache/libelf/libelf-0.8.12.tar.gz
  ==> Fetching from ~/spack/var/spack/cache/libelf/libelf-0.8.12.tar.gz failed.
  ==> Trying to fetch from http://www.mr511.de/software/libelf-0.8.12.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.12-xixqj2vhx6ulmo4lgcqfedtrgrxqziah/libelf-0.8.12.tar.gz
  ==> Created stage in /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.12-xixqj2vhx6ulmo4lgcqfedtrgrxqziah
  ==> Ran patch() for libelf
  ==> Building libelf [AutotoolsPackage]
  ==> Executing phase : 'autoreconf'
  ==> Executing phase : 'configure'
  ==> Executing phase : 'build'
  ==> Executing phase : 'install'
  ==> Successfully installed libelf
  Fetch: 0.00s.  Build: 24.94s.  Total: 24.95s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libelf-0.8.12-xixqj2vhx6ulmo4lgcqfedtrgrxqziah


  $ spack install libelf -j4 %intel@16.0.3.210
  ==> Installing libelf
  ==> Trying to fetch from ~/spack/var/spack/cache/libelf/libelf-0.8.13.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.13-wida7rl47ixpaffk7ygeaui4qnjoxwq4/libelf-0.8.13.tar.gz
  ==> Created stage in /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.13-wida7rl47ixpaffk7ygeaui4qnjoxwq4
  ==> Ran patch() for libelf
  ==> Building libelf [AutotoolsPackage]
  ==> Executing phase : 'autoreconf'
  ==> Executing phase : 'configure'
  ==> Executing phase : 'build'
  ==> Executing phase : 'install'
  ==> Successfully installed libelf
  Fetch: 2.42s.  Build: 58.38s.  Total: 1m 0.80s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/intel-16.0.3.210/libelf-0.8.13-wida7rl47ixpaffk7ygeaui4qnjoxwq4

The spec syntax also includes compiler flags. Spack accepts ``cppflags``,
``cflags``, ``cxxflags``, ``fflags``, ``ldflags``, and ``ldlibs``
parameters.  The values of these fields must be escape-quoted with ``\"``
on the command line. These values are injected into the compile line
automatically by the Spack compiler wrappers.

.. code-block:: console

  $ spack install libelf @0.8.12 cppflags=\"-O3\"
  ==> Installing libelf
  ==> Trying to fetch from ~/spack/var/spack/cache/libelf/libelf-0.8.12.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.12-zejhq6jzj7j6u52ztskw3jpiservkll3/libelf-0.8.12.tar.gz
  ==> Created stage in /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.12-zejhq6jzj7j6u52ztskw3jpiservkll3
  ==> Ran patch() for libelf
  ==> Building libelf [AutotoolsPackage]
  ==> Executing phase : 'autoreconf'
  ==> Executing phase : 'configure'
  ==> Executing phase : 'build'
  ==> Executing phase : 'install'
  ==> Successfully installed libelf
  Fetch: 0.00s.  Build: 12.99s.  Total: 13.00s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libelf-0.8.12-zejhq6jzj7j6u52ztskw3jpiservkll3

The ``spack find`` command is used to query installed packages. Note that
some packages appear identical with the default output. The ``-l`` flag
shows the hash of each package, and the ``-f`` flag shows any non-empty
compiler flags of those packages.

.. code-block:: console

  $ spack find
  ==> 5 installed packages.
  -- cray-CNL-haswell / gcc@6.2.0 -----------------------------
  libelf@0.8.12  libelf@0.8.12  libelf@0.8.13

  -- cray-CNL-haswell / intel@16.0.3.210 --------------------------
  libelf@0.8.13

  -- cray-CNL-haswell / intel@17.0.1.132 --------------------------
  libelf@0.8.13


  $ spack find -lf
    ==> 5 installed packages.
    -- cray-CNL-haswell / gcc@6.2.0 ---------------------------------
    xixqj2v libelf@0.8.12%gcc

    zejhq6j libelf@0.8.12%gcc cppflags="-O3"

    bkwhzge libelf@0.8.13%gcc


    -- cray-CNL-haswell / intel@16.0.3.210 --------------------------
    wida7rl libelf@0.8.13%intel


    -- cray-CNL-haswell / intel@17.0.1.132 --------------------------
    ununouu libelf@0.8.13%intel

Spack generates a hash for each spec. This hash is a function of the full
provenance of the package, so any change to the spec affects the
hash. Spack uses this value to compare specs and to generate unique
installation directories for every combinatorial version. As we move into
more complicated packages with software dependencies, we can see that
Spack reuses existing packages to satisfy a dependency only when the
existing package's hash matches the desired spec.

.. code-block:: console

  $ spack install libdwarf
  ==> Installing libdwarf
  ==> libelf is already installed in ~/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libelf-0.8.13-csrt4qxfkhjgn5xg3zjpkir7xdnszl2a
  ==> Can not find version 20160507 in url_list
  ==> Trying to fetch from ~/spack/var/spack/cache/libdwarf/libdwarf-20160507.tar.gz
  curl: (37) Couldn't open file ~/spack/var/spack/cache/libdwarf/libdwarf-20160507.tar.gz
  ==> Fetching from ~/spack/var/spack/cache/libdwarf/libdwarf-20160507.tar.gz failed.
  ==> Trying to fetch from http://www.prevanders.net/libdwarf-20160507.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: /global/u2/m/mamelara/spack/var/spack/stage/libdwarf-20160507-3l5dfjjltgajfmgv4ev3b56pgqxwnnwu/libdwarf-20160507.tar.gz
  ==> Created stage in /global/u2/m/mamelara/spack/var/spack/stage/libdwarf-20160507-3l5dfjjltgajfmgv4ev3b56pgqxwnnwu
  ==> No patches needed for libdwarf
  ==> Building libdwarf [Package]
  ==> Executing phase : 'install'
  ==> Successfully installed libdwarf
  Fetch: 0.01s.  Build: 1m 10.21s.  Total: 1m 10.22s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libdwarf-20160507-3l5dfjjltgajfmgv4ev3b56pgqxwnnwu


Dependencies can be explicitly requested using the ``^`` sigil. Note that
the spec syntax is recursive. Anything we could specify about the
top-level package, we can also specify about a dependency using ``^``.

.. code-block:: console

  $ spack install libdwarf ^libelf @0.8.12 %intel
  ==> Installing libdwarf
  ==> Installing libelf
  ==> Trying to fetch from ~/spack/var/spack/cache/libelf/libelf-0.8.12.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.12-vrvy4lwumuqv5td7zx6gq32cu45hfca6/libelf-0.8.12.tar.gz
  ==> Created stage in /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.12-vrvy4lwumuqv5td7zx6gq32cu45hfca6
  ==> Ran patch() for libelf
  ==> Building libelf [AutotoolsPackage]
  ==> Executing phase : 'autoreconf'
  ==> Executing phase : 'configure'
  ==> Executing phase : 'build'
  ==> Executing phase : 'install'
  ==> Successfully installed libelf
    Fetch: 0.01s.  Build: 54.15s.  Total: 54.15s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/intel-17.0.1.132/libelf-0.8.12-vrvy4lwumuqv5td7zx6gq32cu45hfca6
  ==> Can not find version 20160507 in url_list
  ==> Trying to fetch from ~/spack/var/spack/cache/libdwarf/libdwarf-20160507.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: /global/u2/m/mamelara/spack/var/spack/stage/libdwarf-20160507-xlrd5sqcswzpiwykr23272ljfezsqudo/libdwarf-20160507.tar.gz
  ==> Created stage in /global/u2/m/mamelara/spack/var/spack/stage/libdwarf-20160507-xlrd5sqcswzpiwykr23272ljfezsqudo
  ==> No patches needed for libdwarf
  ==> Building libdwarf [Package]
  ==> Executing phase : 'install'
  ==> Successfully installed libdwarf
    Fetch: 0.01s.  Build: 3m 39.96s.  Total: 3m 39.97s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/intel-17.0.1.132/libdwarf-20160507-xlrd5sqcswzpiwykr23272ljfezsqudo

Packages can also be referred to from the command line by their package
hash. Using the ``spack find -lf`` command earlier we saw that the hash
of our optimized installation of libelf (``cppflags=\"-O3\"``) began with
``zejhq6j``. We can now explicitly build with that package without typing
the entire spec, by using the ``/`` sigil to refer to it by hash. As with
other tools like git, you do not need to specify an *entire* hash on the
command line.  You can specify just enough digits to identify a hash
uniquely.  If a hash prefix is ambiguous (i.e., two or more installed
packages share the prefix) then spack will report an error.

.. code-block:: console

  $ spack install libdwarf ^/zejhq6j
  ==> Installing libdwarf
  ==> libelf is already installed in ~/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libelf-0.8.12-vrv2ttbd34xlfoxy4jwt6qsjrcbalmmw
  ==> Can not find version 20160507 in url_list
  ==> Trying to fetch from ~/spack/var/spack/cache/libdwarf/libdwarf-20160507.tar.gz
  #################################################################################################################################################################################################################################################### 100.0%
  ==> Staging archive: /global/u2/m/mamelara/spack/var/spack/stage/libdwarf-20160507-ba2loau3i7piwqn54taa2zs6ct4eubys/libdwarf-20160507.tar.gz
  ==> Created stage in /global/u2/m/mamelara/spack/var/spack/stage/libdwarf-20160507-ba2loau3i7piwqn54taa2zs6ct4eubys
  ==> No patches needed for libdwarf
  ==> Building libdwarf [Package]
  ==> Executing phase : 'install'
  ==> Successfully installed libdwarf
    Fetch: 0.01s.  Build: 31.22s.  Total: 31.23s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libdwarf-20160507-ba2loau3i7piwqn54taa2zs6ct4eubys 

The ``spack find`` command can also take a ``-d`` flag, which can show
dependency information. Note that each package has a top-level entry,
even if it also appears as a dependency.

.. code-block:: console

  $ spack find -ldf
  ==> 9 installed packages.
  -- cray-CNL-haswell / gcc@6.2.0 ---------------------------------
  ba2loau    libdwarf@20160507%gcc
  zejhq6j        ^libelf@0.8.12%gcc cppflags="-O3"

  3l5dfjj    libdwarf@20160507%gcc
  bkwhzge        ^libelf@0.8.13%gcc

  xixqj2v    libelf@0.8.12%gcc

  zejhq6j    libelf@0.8.12%gcc cppflags="-O3"

  bkwhzge    libelf@0.8.13%gcc


  -- cray-CNL-haswell / intel@16.0.3.210 --------------------------
  wida7rl    libelf@0.8.13%intel


  -- cray-CNL-haswell / intel@17.0.1.132 --------------------------
  xlrd5sq    libdwarf@20160507%intel
  vrvy4lw        ^libelf@0.8.12%intel

  vrvy4lw    libelf@0.8.12%intel

  ununouu    libelf@0.8.13%intel

As we get to more complex packages, full installs will take too long to
build in the time allotted for this tutorial. Our collaborators at CERN
have been working on binary caching for Spack, which would allow for very
fast installs of previously built packages. We are still working out the
security ramifications of the feature, but it is coming soon.

For now, we will switch to doing "fake" installs. When supplied with the
``--fake`` flag (primarily used for debugging), Spack computes build
metadata the same way it normally would, but it does not download the
source or run the install script for a pacakge. We can use this to
quickly demonstrate some of the more advanced Spack features in our
limited tutorial time.

``HDF5`` is an example of a more complicated package, with an MPI
dependency. If we install it "out of the box," it will build with
``openmpi``.

.. code-block:: console

  spack install --fake hdf5
  ==> Installing hdf5
  ==> Installing zlib
  ==> Building zlib [AutotoolsPackage]
  ==> Successfully installed zlib
  Fetch: .  Build: 0.12s.  Total: 0.12s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/zlib-1.2.8-vnwrdo3al6hojzwcf6wf2rr32skvmw45
  ==> Installing openmpi
  ==> Installing hwloc
  ==> Installing libpciaccess
  ==> Installing util-macros
  ==> Building util-macros [Package]
  ==> Successfully installed util-macros
  Fetch: .  Build: 0.12s.  Total: 0.12s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/util-macros-1.19.0-ojeaursjlw3wxrd5dtkkhnovnomej75v
  ==> Installing libtool
  ==> Installing m4
  ==> Installing libsigsegv
  ==> Building libsigsegv [AutotoolsPackage]
  ==> Successfully installed libsigsegv
  Fetch: .  Build: 0.09s.  Total: 0.09s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libsigsegv-2.10-cro3222hkjvzqoj4wa7ly2rqf7bisdoc
  ==> Building m4 [AutotoolsPackage]
  ==> Successfully installed m4
  Fetch: .  Build: 0.17s.  Total: 0.17s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/m4-1.4.17-ixzoggem36bu3hjojtd2i3e6wc5gbqyh
  ==> Building libtool [AutotoolsPackage]
  ==> Successfully installed libtool
  Fetch: .  Build: 0.09s.  Total: 0.09s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libtool-2.4.6-rt7axrxfbcievmeswzvmwfcmdkvrrk4e
  ==> pkg-config is externally installed in /usr/bin/pkg-config
  ==> Building libpciaccess [Package]
  ==> Successfully installed libpciaccess
  Fetch: .  Build: 0.13s.  Total: 0.13s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libpciaccess-0.13.4-akapxtmzggm5ono2bxmldw36aobt7rep
  ==> Building hwloc [Package]
  ==> Successfully installed hwloc
  Fetch: .  Build: 0.18s.  Total: 0.18s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hwloc-1.11.4-djmeswyv7adqjhuzfyoh527a7ewyvkit
  ==> Building openmpi [AutotoolsPackage]
  ==> Successfully installed openmpi
  Fetch: .  Build: 0.29s.  Total: 0.29s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openmpi-2.0.1-6vi4ni5z7l4pihbugck6rdylnzuws4ak
  ==> Building hdf5 [AutotoolsPackage]
  ==> Successfully installed hdf5
  Fetch: .  Build: 0.43s.  Total: 0.43s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hdf5-1.10.0-patch1-oftj7ewtw7dx4dw7o35sdkeqxfvvkxnn

Spack packages can also have variants. Boolean variants can be specified
using the ``+`` and ``~`` or ``-`` sigils. There are two sigils for
``False`` to avoid conflicts with shell parsing in different
situations. Variants (boolean or otherwise) can also be specified using
the same syntax as compiler flags.  Here we can install HDF5 without MPI
support.

.. code-block:: console

  spack install --fake hdf5~mpi
  ==> Installing hdf5
  ==> zlib is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/zlib-1.2.8-vnwrdo3al6hojzwcf6wf2rr32skvmw45
  ==> Building hdf5 [AutotoolsPackage]
  ==> Successfully installed hdf5
    Fetch: .  Build: 0.20s.  Total: 0.20s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hdf5-1.10.0-patch1-axmycpvg3d5mdxyxiydq6aqw2kdzbxks


We might also want to install HDF5 with a different MPI
implementation. While MPI is not a package itself, packages can depend on
abstract interfaces like MPI. Spack handles these through "virtual
dependencies." A package, such as HDF5, can depend on the MPI
interface. Other packages (``openmpi``, ``mpich``, ``mvapich``, etc.)
provide the MPI interface.  Any of these providers can be requested for
an MPI dependency. For example, we can build HDF5 with MPI support
provided by mpich by specifying a dependency on ``mpich``. Spack also
supports versioning of virtual dependencies. A package can depend on the
MPI interface at version 3, and provider packages specify what version of
the interface *they* provide. The partial spec ``^mpi@3`` can be safisfied
by any of several providers.

.. code-block:: console
  $ spack install --fake hdf5+mpi ^mpich
  ==> Installing hdf5
  ==> Installing mpich
  ==> Building mpich [AutotoolsPackage]
  ==> Successfully installed mpich
    Fetch: .  Build: 0.09s.  Total: 0.09s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mpich-3.2-6zlz4tveokpsolm4c4fb7vybtvlwt7qa
  ==> zlib is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/zlib-1.2.8-vnwrdo3al6hojzwcf6wf2rr32skvmw45
  ==> Building hdf5 [AutotoolsPackage]
  ==> Successfully installed hdf5
    Fetch: .  Build: 0.20s.  Total: 0.20s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hdf5-1.10.0-patch1-blx6lqfvfq7plwj4q7adsd4x7mwwxppp

We'll do a quick check in on what we have installed so far.

.. code-block:: console
  ==> 21 installed packages.
  -- cray-CNL-haswell / gcc@6.2.0 ---------------------------------
  axmycpv    hdf5@1.10.0-patch1%gcc
  vnwrdo3        ^zlib@1.2.8%gcc

  blx6lqf    hdf5@1.10.0-patch1%gcc
  6zlz4tv        ^mpich@3.2%gcc
  vnwrdo3        ^zlib@1.2.8%gcc

  oftj7ew    hdf5@1.10.0-patch1%gcc
  6vi4ni5        ^openmpi@2.0.1%gcc
  djmeswy            ^hwloc@1.11.4%gcc
  akapxtm                ^libpciaccess@0.13.4%gcc
  vnwrdo3        ^zlib@1.2.8%gcc

  djmeswy    hwloc@1.11.4%gcc
  akapxtm        ^libpciaccess@0.13.4%gcc

  ba2loau    libdwarf@20160507%gcc
  zejhq6j        ^libelf@0.8.12%gcc cppflags="-O3"

  3l5dfjj    libdwarf@20160507%gcc
  bkwhzge        ^libelf@0.8.13%gcc

  xixqj2v    libelf@0.8.12%gcc

  zejhq6j    libelf@0.8.12%gcc cppflags="-O3"

  bkwhzge    libelf@0.8.13%gcc

  akapxtm    libpciaccess@0.13.4%gcc

  cro3222    libsigsegv@2.10%gcc

  rt7axrx    libtool@2.4.6%gcc

  ixzogge    m4@1.4.17%gcc
  cro3222        ^libsigsegv@2.10%gcc

  6zlz4tv    mpich@3.2%gcc

  6vi4ni5    openmpi@2.0.1%gcc
  djmeswy        ^hwloc@1.11.4%gcc
  akapxtm            ^libpciaccess@0.13.4%gcc

  ojeaurs    util-macros@1.19.0%gcc

  vnwrdo3    zlib@1.2.8%gcc


  -- cray-CNL-haswell / intel@16.0.3.210 --------------------------
  wida7rl    libelf@0.8.13%intel


  -- cray-CNL-haswell / intel@17.0.1.132 --------------------------
  xlrd5sq    libdwarf@20160507%intel
  vrvy4lw        ^libelf@0.8.12%intel

  vrvy4lw    libelf@0.8.12%intel

  ununouu    libelf@0.8.13%intel

Spack models the dependencies of packages as a directed acyclic graph
(DAG). The ``spack find -d`` command shows the tree representation of
that graph.  We can also use the ``spack graph`` command to view the entire
DAG as a graph.

.. code-block:: console

  $ spack graph hdf5+mpi ^mpich
  o  hdf5
  |\
  o |  zlib
   /
  o  mpich

You may also have noticed that there are some packages shown in the
``spack find -d`` output that we didn't install explicitly. These are
dependencies that were installed implicitly. A few packages installed
implicitly are not shown as dependencies in the ``spack find -d``
output. These are build dependencies. For example, ``libpciaccess`` is a
dependency of openmpi and requires m4 to build. Spack will build `m4`` as
part of the installation of ``openmpi``, but it does not become a part of
the DAG because it is not linked in at run time. Spack handles build
dependencies differently because of their different (less strict)
consistency requirements. It is entirely possible to have two packages
using different versions of a dependency to build, which obviously cannot
be done with linked dependencies.

``HDF5`` is more complicated than our basic example of libelf and
libdwarf, but it's still within the realm of software that an experienced
HPC user could reasonably expect to install given a bit of time. Now
let's look at a more complicated package.

.. code-block:: console

  $ spack install --fake trilinos
  ==> Installing trilinos
  ==> Installing superlu-dist
  ==> openmpi is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openmpi-2.0.1-6vi4ni5z7l4pihbugck6rdylnzuws4ak
  ==> Installing parmetis
  ==> openmpi is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openmpi-2.0.1-6vi4ni5z7l4pihbugck6rdylnzuws4ak
  ==> Installing cmake
  ==> Installing ncurses
  ==> Building ncurses [Package]
  ==> Successfully installed ncurses
  Fetch: .  Build: 0.14s.  Total: 0.14s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/ncurses-6.0-ti24btafu5zwhzgzcy5in43e5weafmyr
  ==> Installing openssl
  ==> zlib is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/zlib-1.2.8-vnwrdo3al6hojzwcf6wf2rr32skvmw45
  ==> Building openssl [Package]
  ==> Successfully installed openssl
  Fetch: .  Build: 0.19s.  Total: 0.19s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openssl-1.0.2j-rtibvnmwjcos263btri3d4lrtucnupa6
  ==> Building cmake [Package]
  ==> Successfully installed cmake
  Fetch: .  Build: 0.33s.  Total: 0.33s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/cmake-3.7.1-groolt4cgfdp5tg64erxu2pui6xtws6w
  ==> Installing metis
  ==> cmake is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/cmake-3.7.1-groolt4cgfdp5tg64erxu2pui6xtws6w
  ==> Building metis [Package]
  ==> Successfully installed metis
  Fetch: .  Build: 0.12s.  Total: 0.12s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/metis-5.1.0-hicw2fyxba7mfatl37mcqnpfazkdrrfg
  ==> Building parmetis [Package]
  ==> Successfully installed parmetis
  Fetch: .  Build: 0.55s.  Total: 0.55s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/parmetis-4.0.3-ueykxwydbhavcg5nlvoecxrl7clz6oby
  ==> Installing openblas
  ==> Building openblas [MakefilePackage]
  ==> Successfully installed openblas
  Fetch: .  Build: 0.09s.  Total: 0.09s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openblas-0.2.19-mm74idshhyfxcnwi3wnubmhg5r6kh4zy
  ==> metis is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/metis-5.1.0-hicw2fyxba7mfatl37mcqnpfazkdrrfg
  ==> Building superlu-dist [Package]
  ==> Successfully installed superlu-dist
  Fetch: .  Build: 0.75s.  Total: 0.75s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/superlu-dist-5.1.1-5c7vjzau6t4xwsg3suzylcp23rpb6a2m
  ==> cmake is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/cmake-3.7.1-groolt4cgfdp5tg64erxu2pui6xtws6w
  ==> Installing glm
  ==> cmake is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/cmake-3.7.1-groolt4cgfdp5tg64erxu2pui6xtws6w
  ==> Building glm [Package]
  ==> Successfully installed glm
  Fetch: .  Build: 0.14s.  Total: 0.14s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/glm-0.9.7.1-mwxf4sfxyzbjb35ubltsrjrvbkavlbkt
  ==> Installing hypre
  ==> openmpi is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openmpi-2.0.1-6vi4ni5z7l4pihbugck6rdylnzuws4ak
  ==> openblas is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openblas-0.2.19-mm74idshhyfxcnwi3wnubmhg5r6kh4zy
  ==> Building hypre [Package]
  ==> Successfully installed hypre
  Fetch: .  Build: 0.46s.  Total: 0.46s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hypre-2.11.1-miedlysnmdrbhlxmsedwwoda7s7ngru7
  ==> metis is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/metis-5.1.0-hicw2fyxba7mfatl37mcqnpfazkdrrfg
  ==> Installing netlib-scalapack
  ==> openmpi is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openmpi-2.0.1-6vi4ni5z7l4pihbugck6rdylnzuws4ak
  ==> cmake is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/cmake-3.7.1-groolt4cgfdp5tg64erxu2pui6xtws6w
  ==> openblas is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openblas-0.2.19-mm74idshhyfxcnwi3wnubmhg5r6kh4zy
  ==> Building netlib-scalapack [Package]
  ==> Successfully installed netlib-scalapack
  Fetch: .  Build: 0.47s.  Total: 0.47s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/netlib-scalapack-2.0.2-gfj6bxd6z33u52aiv6gxt45bikcdfyfe
  ==> Installing suite-sparse
  ==> Installing tbb
  ==> Building tbb [Package]
  ==> Successfully installed tbb
  Fetch: .  Build: 0.09s.  Total: 0.09s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/tbb-2017.3-gsc4orgvu5jnxab6ywcpuxuhwkeztnlc
  ==> openblas is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openblas-0.2.19-mm74idshhyfxcnwi3wnubmhg5r6kh4zy
  ==> metis is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/metis-5.1.0-hicw2fyxba7mfatl37mcqnpfazkdrrfg
  ==> Building suite-sparse [Package]
  ==> Successfully installed suite-sparse
  Fetch: .  Build: 0.38s.  Total: 0.38s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/suite-sparse-4.5.3-2udlijaisvewibo6harw3kimhttil2td
  ==> openmpi is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openmpi-2.0.1-6vi4ni5z7l4pihbugck6rdylnzuws4ak
  ==> netcdf is externally installed in /opt/cray/pe/netcdf/4.4.1/GNU/5.1
  ==> Installing mumps
  ==> netlib-scalapack is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/netlib-scalapack-2.0.2-gfj6bxd6z33u52aiv6gxt45bikcdfyfe
  ==> openmpi is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openmpi-2.0.1-6vi4ni5z7l4pihbugck6rdylnzuws4ak
  ==> openblas is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openblas-0.2.19-mm74idshhyfxcnwi3wnubmhg5r6kh4zy
  ==> Building mumps [Package]
  ==> Successfully installed mumps
  Fetch: .  Build: 0.57s.  Total: 0.57s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mumps-5.0.2-yrl4i6jadjvm6l7vqtt3zvyu4gahyx2h
  ==> Installing matio
  ==> zlib is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/zlib-1.2.8-vnwrdo3al6hojzwcf6wf2rr32skvmw45
  ==> hdf5 is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hdf5-1.10.0-patch1-oftj7ewtw7dx4dw7o35sdkeqxfvvkxnn
  ==> Building matio [AutotoolsPackage]
  ==> Successfully installed matio
  Fetch: .  Build: 0.53s.  Total: 0.53s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/matio-1.5.9-kdwi6ggu4d6bbb7hawos6gmwdtmev6fz
  ==> Installing boost
  ==> Installing bzip2
  ==> Building bzip2 [Package]
  ==> Successfully installed bzip2
  Fetch: .  Build: 0.14s.  Total: 0.14s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/bzip2-1.0.6-js6dsfr4ifivstb2bdx6zv5wxddgn3u2
  ==> zlib is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/zlib-1.2.8-vnwrdo3al6hojzwcf6wf2rr32skvmw45
  ==> Building boost [Package]
  ==> Successfully installed boost
  Fetch: .  Build: 0.27s.  Total: 0.27s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/boost-1.62.0-ts3d2trvn6du2n2kcjgbhiwkde3v2upt
  ==> parmetis is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/parmetis-4.0.3-ueykxwydbhavcg5nlvoecxrl7clz6oby
  ==> openblas is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openblas-0.2.19-mm74idshhyfxcnwi3wnubmhg5r6kh4zy
  ==> hdf5 is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hdf5-1.10.0-patch1-oftj7ewtw7dx4dw7o35sdkeqxfvvkxnn
  ==> Building trilinos [CMakePackage]
  ==> Successfully installed trilinos
  Fetch: .  Build: 2.18s.  Total: 2.18s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/trilinos-12.10.1-tb3x3fpq564mozkkkcbt4v6bpopi2loz

Now we're starting to see the power of Spack. Trilinos has 11 top level
dependecies, many of which have dependencies of their own. Installing
more complex packages can take days or weeks even for an experienced
user. Although we've done a fake installation for the tutorial, a real
installation of trilinos using Spack takes about 3 hours (depending on
the system), but only 20 seconds of programmer time.

Spack manages constistency of the entire DAG. Every MPI dependency will
be satisfied by the same configuration of MPI, etc. If we install
``trilinos`` again specifying a dependency on our previous HDF5 built
with ``mpich``:

.. code-block:: console

  $ spack install --fake trilinos ^hdf5+mpi ^mpich
    ==> Installing trilinos
    ==> Installing superlu-dist
    ==> mpich is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mpich-3.2-6zlz4tveokpsolm4c4fb7vybtvlwt7qa
    ==> metis is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/metis-5.1.0-hicw2fyxba7mfatl37mcqnpfazkdrrfg
    ==> Installing parmetis
    ==> mpich is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mpich-3.2-6zlz4tveokpsolm4c4fb7vybtvlwt7qa
    ==> metis is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/metis-5.1.0-hicw2fyxba7mfatl37mcqnpfazkdrrfg
    ==> cmake is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/cmake-3.7.1-groolt4cgfdp5tg64erxu2pui6xtws6w
    ==> Building parmetis [Package]
    ==> Successfully installed parmetis
      Fetch: .  Build: 0.34s.  Total: 0.34s.
    [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/parmetis-4.0.3-anb7yswybmszhofapro5avhgsqtc5dbm
    ==> openblas is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openblas-0.2.19-mm74idshhyfxcnwi3wnubmhg5r6kh4zy
    ==> Building superlu-dist [Package]
    ==> Successfully installed superlu-dist
      Fetch: .  Build: 0.49s.  Total: 0.49s.
    [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/superlu-dist-5.1.1-asxd3ehyyl3t3fobzzguuh7e24sh2qp4
    ==> cmake is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/cmake-3.7.1-groolt4cgfdp5tg64erxu2pui6xtws6w
    ==> glm is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/glm-0.9.7.1-mwxf4sfxyzbjb35ubltsrjrvbkavlbkt
    ==> Installing hypre
    ==> mpich is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mpich-3.2-6zlz4tveokpsolm4c4fb7vybtvlwt7qa
    ==> openblas is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openblas-0.2.19-mm74idshhyfxcnwi3wnubmhg5r6kh4zy
    ==> Building hypre [Package]
    ==> Successfully installed hypre
      Fetch: .  Build: 0.25s.  Total: 0.25s.
    [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hypre-2.11.1-7rgpm4j4la3t7fy7sb2gdfhdushopjw4
    ==> metis is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/metis-5.1.0-hicw2fyxba7mfatl37mcqnpfazkdrrfg
    ==> Installing netlib-scalapack
    ==> mpich is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mpich-3.2-6zlz4tveokpsolm4c4fb7vybtvlwt7qa
    ==> cmake is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/cmake-3.7.1-groolt4cgfdp5tg64erxu2pui6xtws6w
    ==> openblas is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openblas-0.2.19-mm74idshhyfxcnwi3wnubmhg5r6kh4zy
    ==> Building netlib-scalapack [Package]
    ==> Successfully installed netlib-scalapack
    Fetch: .  Build: 0.24s.  Total: 0.24s.
    [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/netlib-scalapack-2.0.2-7bc2uzwei7unu7pqz32znncp4kkea5ea
    ==> suite-sparse is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/suite-sparse-4.5.3-2udlijaisvewibo6harw3kimhttil2td
    ==> netcdf is externally installed in /opt/cray/pe/netcdf/4.4.1/GNU/5.1
    ==> Installing mumps
    ==> mpich is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mpich-3.2-6zlz4tveokpsolm4c4fb7vybtvlwt7qa
    ==> netlib-scalapack is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/netlib-scalapack-2.0.2-7bc2uzwei7unu7pqz32znncp4kkea5ea
    ==> openblas is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openblas-0.2.19-mm74idshhyfxcnwi3wnubmhg5r6kh4zy
    ==> Building mumps [Package]
    ==> Successfully installed mumps
      Fetch: .  Build: 0.34s.  Total: 0.34s.
    [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mumps-5.0.2-andq4bkq5czbzhdwvqafag23zs2v5meg
    ==> mpich is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mpich-3.2-6zlz4tveokpsolm4c4fb7vybtvlwt7qa
    ==> Installing matio
    ==> zlib is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/zlib-1.2.8-vnwrdo3al6hojzwcf6wf2rr32skvmw45
    ==> hdf5 is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hdf5-1.10.0-patch1-blx6lqfvfq7plwj4q7adsd4x7mwwxppp
    ==> Building matio [AutotoolsPackage]
    ==> Successfully installed matio
      Fetch: .  Build: 0.25s.  Total: 0.25s.
    [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/matio-1.5.9-ozit2bfc5bj7nvyoyd42h6ar53kqdyv4
    ==> boost is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/boost-1.62.0-ts3d2trvn6du2n2kcjgbhiwkde3v2upt
    ==> parmetis is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/parmetis-4.0.3-anb7yswybmszhofapro5avhgsqtc5dbm
    ==> openblas is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openblas-0.2.19-mm74idshhyfxcnwi3wnubmhg5r6kh4zy
    ==> hdf5 is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hdf5-1.10.0-patch1-blx6lqfvfq7plwj4q7adsd4x7mwwxppp
    ==> Building trilinos [CMakePackage]
    ==> Successfully installed trilinos
      Fetch: .  Build: 1.74s.  Total: 1.74s.
    [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/trilinos-12.10.1-lian6yd4o67oszehn4v52x5ftkyaysdb

We see that every package in the trilinos DAG that depends on MPI now
uses ``mpich``.

.. code-block:: console

  $ spack find -d trilinos
  ==> 2 installed packages.
  -- cray-CNL-haswell / gcc@6.2.0 -----------------------------
      trilinos@12.8.1
          ^boost@1.62.0
              ^bzip2@1.0.6
              ^zlib@1.2.8
          ^glm@0.9.7.1
          ^hdf5@1.10.0-patch1
              ^mpich@3.2
          ^hypre@2.11.1
              ^openblas@0.2.19
          ^matio@1.5.2
          ^metis@5.1.0
          ^mumps@5.0.2
              ^netlib-scalapack@2.0.2
          ^netcdf@4.4.1
              ^curl@7.50.3
                  ^openssl@1.0.2j
          ^parmetis@4.0.3
          ^suite-sparse@4.5.3
              ^tbb@4.4.4
          ^superlu-dist@5.1.1

      trilinos@12.8.1
          ^boost@1.62.0
              ^bzip2@1.0.6
              ^zlib@1.2.8
          ^glm@0.9.7.1
          ^hdf5@1.10.0-patch1
              ^openmpi@2.0.1
                  ^hwloc@1.11.4
                      ^libpciaccess@0.13.4
          ^hypre@2.11.1
              ^openblas@0.2.19
          ^matio@1.5.2
          ^metis@5.1.0
          ^mumps@5.0.2
              ^netlib-scalapack@2.0.2
          ^netcdf@4.4.1
              ^curl@7.50.3
                  ^openssl@1.0.2j
          ^parmetis@4.0.3
          ^suite-sparse@4.5.3
              ^tbb@4.4.4
          ^superlu-dist@5.1.1


As we discussed before, the ``spack find -d`` command shows the
dependency information as a tree. While that is often sufficient, many
complicated packages, including trilinos, have dependencies that
cannot be fully represented as a tree. Again, the ``spack graph``
command shows the full DAG of the dependency information.

.. code-block:: console

  $ spack graph trilinos
  o  trilinos
  |\
  | |\
  | | |\
  | | | |\
  | | | | |\
  | | | | | |\
  | | | | | | |\
  | o | | | | | |  netcdf
  | |\ \ \ \ \ \ \
  | | |\ \ \ \ \ \ \
  | | | o | | | | | |  curl
  | | |/| | | | | | |
  | |/| | | | | | | |
  | | | o | | | | | |  openssl
  | | |/ / / / / / /
  | |/| | | | | | |
  | | o | | | | | |  hdf5
  | |/| | | | | | |
  | | |/ / / / / /
  | o | | | | | |  zlib
  |  / / / / / /
  o | | | | | |  swig
  o | | | | | |  pcre
   / / / / / /
  o | | | | |  mpi
   / / / / /
  o | | | |  matio
   / / / /
  o | | |  lapack
   / / /
  o | |  glm
   / /
  o |  boost
   /
  o  blas


You can control how the output is displayed with a number of options.

The ASCII output from ``spack graph`` can be difficult to parse for
complicated packages. The output can be changed to the ``graphviz``
``.dot`` format using the `--dot` flag.

.. code-block:: console

  $ spack graph --dot trilinos | dot -Tpdf trilinos_graph.pdf

.. _basics-tutorial-uninstall:

---------------------
Uninstalling Packages
---------------------

Earlier we installed many configurations each of libelf and
libdwarf. Now we will go through and uninstall some of those packages
that we didn't really need.

.. code-block:: console

  $ spack find -d libdwarf
  ==> 3 installed packages.
  -- cray-CNL-haswell / gcc@6.2.0-----------------------------
      libdwarf@20160507
          ^libelf@0.8.12

      libdwarf@20160507
          ^libelf@0.8.13


  -- cray-CNL-haswell / intel@17.0.1.132 --------------------------
      libdwarf@20160507
          ^libelf@0.8.12

  $ spack find libelf
  ==> 6 installed packages.
  -- cray-CNL-haswell / gcc@6.2.0 -----------------------------
  libelf@0.8.12  libelf@0.8.12  libelf@0.8.13

  -- cray-CNL-haswell / intel@16.0.3.210 --------------------------
  libelf@0.8.13

  -- cray-CNL-haswell / intel@17.0.1.132 --------------------------
  libelf@0.8.12  libelf@0.8.13


We can uninstall packages by spec using the same syntax as install.

.. code-block:: console

  $ spack uninstall libelf%intel@16.0.3.210
  ==> The following packages will be uninstalled :

  -- cray-CNL-haswell / intel@16.0.3.210 --------------------------
  wida7rl libelf@0.8.13%intel


  ==> Do you want to proceed ? [y/n]
  y
  ==> Successfully uninstalled libelf@0.8.13%intel@16.0.3.210 arch=cray-CNL-haswell-wida7rl


  $ spack find -lf libelf
  ==> 5 installed packages.
  -- cray-CNL-haswell / gcc@6.2.0 ---------------------------------
  xixqj2v libelf@0.8.12%gcc

  zejhq6j libelf@0.8.12%gcc cppflags="-O3"

  bkwhzge libelf@0.8.13%gcc


  -- cray-CNL-haswell / intel@17.0.1.132 --------------------------
  vrvy4lw libelf@0.8.12%intel

  ununouu libelf@0.8.13%intel

We can uninstall packages by referring only to their hash.


We can use either ``-f`` (force) or ``-d`` (remove dependents as well) to
remove packages that are required by another installed package.

.. code-block:: console

  $ spack uninstall /vrvy
  ==> Error: Will not uninstall libelf@0.8.12%intel@17.0.1.132-vrvy4lw

  The following packages depend on it:
  -- cray-CNL-haswell / intel@17.0.1.132 --------------------------
  xlrd5sq libdwarf@20160507%intel

  ==> Error: You can use spack uninstall --dependents to uninstall these dependencies as well

  $ spack uninstall -d /vrvy
  ==> The following packages will be uninstalled :

  -- cray-CNL-haswell / intel@17.0.1.132 --------------------------
  xlrd5sq libdwarf@20160507%intel

  vrvy4lw libelf@0.8.12%intel

  ==> Do you want to proceed ? [y/n]
  y
  ==> Successfully uninstalled libdwarf@20160507%intel@17.0.1.132 arch=cray-CNL-haswell-xlrd5sq
  ==> Successfully uninstalled libelf@0.8.12%intel@17.0.1.132 arch=cray-CNL-haswell-vrvy4lw

Spack will not uninstall packages that are not sufficiently
specified. The ``-a`` (all) flag can be used to uninstall multiple
packages at once.

.. code-block:: console

  $ spack uninstall trilinos
  ==> Error: trilinos matches multiple packages:

  -- cray-CNL-haswell / gcc@6.2.0 ---------------------------------
  lian6yd trilinos@12.10.1%gcc+boost~debug+hdf5+hypre+metis+mumps~python+shared+suite-sparse~superlu+superlu-dist~xsdkflags

  tb3x3fp trilinos@12.10.1%gcc+boost~debug+hdf5+hypre+metis+mumps~python+shared+suite-sparse~superlu+superlu-dist~xsdkflags


  ==> Error: You can either:
      a) Use a more specific spec, or
      b) use spack uninstall -a to uninstall ALL matching specs.


  $ spack uninstall /lian
  ==> The following packages will be uninstalled :

  -- cray-CNL-haswell / gcc@6.2.0 ---------------------------------
  lian6yd trilinos@12.10.1%gcc+boost~debug+hdf5+hypre+metis+mumps~python+shared+suite-sparse~superlu+superlu-dist~xsdkflags


  ==> Do you want to proceed ? [y/n]
  y
  ==> Successfully uninstalled trilinos@12.10.1%gcc@6.2.0+boost~debug+hdf5+hypre+metis+mumps~python+shared+suite-sparse~superlu+superlu-dist~xsdkflags arch=cray-CNL-haswell-lian6yd

-----------------------------
Advanced ``spack find`` Usage
-----------------------------

We will go over some additional uses for the `spack find` command not
already covered in the :ref:`basics-tutorial-install` and
:ref:`basics-tutorial-uninstall` sections.

The ``spack find`` command can accept what we call "anonymous specs."
These are expressions in spec syntax that do not contain a package
name. For example, `spack find %intel` will return every package built
with the intel compiler, and ``spack find cppflags=\\"-O3\\"`` will
return every package which was built with ``cppflags=\\"-O3\\"``.

.. code-block:: console

  $ spack find %intel
  ==> 1 installed packages.
  -- cray-CNL-haswell / intel@17.0.1.132 --------------------------
  libelf@0.8.13



  $ spack find cppflags=\"-O3\"
  ==> 1 installed packages.
  -- cray-CNL-haswell / gcc@4.4.7 -----------------------------
  libelf@0.8.12


The ``find`` command can also show which packages were installed
explicitly (rather than pulled in as a dependency) using the ``-e``
flag. The ``-E`` flag shows implicit installs only. The ``find`` command can
also show the path to which a spack package was installed using the ``-p``
command.

.. code-block:: console
  $ spack find -pe
  ==> 41 installed packages.
  -- cray-CNL-haswell / gcc@6.2.0 ---------------------------------
  boost@1.62.0            /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/boost-1.62.0-ts3d2trvn6du2n2kcjgbhiwkde3v2upt
  bzip2@1.0.6             /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/bzip2-1.0.6-js6dsfr4ifivstb2bdx6zv5wxddgn3u2
  cmake@3.7.1             /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/cmake-3.7.1-groolt4cgfdp5tg64erxu2pui6xtws6w
  glm@0.9.7.1             /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/glm-0.9.7.1-mwxf4sfxyzbjb35ubltsrjrvbkavlbkt
  hdf5@1.10.0-patch1      /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hdf5-1.10.0-patch1-axmycpvg3d5mdxyxiydq6aqw2kdzbxks
  hdf5@1.10.0-patch1      /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hdf5-1.10.0-patch1-blx6lqfvfq7plwj4q7adsd4x7mwwxppp
  hdf5@1.10.0-patch1      /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hdf5-1.10.0-patch1-oftj7ewtw7dx4dw7o35sdkeqxfvvkxnn
  hwloc@1.11.4            /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hwloc-1.11.4-djmeswyv7adqjhuzfyoh527a7ewyvkit
  hypre@2.11.1            /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hypre-2.11.1-7rgpm4j4la3t7fy7sb2gdfhdushopjw4
  hypre@2.11.1            /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/hypre-2.11.1-miedlysnmdrbhlxmsedwwoda7s7ngru7
  libdwarf@20160507       /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libdwarf-20160507-ba2loau3i7piwqn54taa2zs6ct4eubys
  libdwarf@20160507       /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libdwarf-20160507-3l5dfjjltgajfmgv4ev3b56pgqxwnnwu
  libelf@0.8.12           /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libelf-0.8.12-xixqj2vhx6ulmo4lgcqfedtrgrxqziah
  libelf@0.8.12           /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libelf-0.8.12-zejhq6jzj7j6u52ztskw3jpiservkll3
  libelf@0.8.13           /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libelf-0.8.13-bkwhzgecutmhfzo2fsaybsya2ldhxgjf
  libpciaccess@0.13.4     /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libpciaccess-0.13.4-akapxtmzggm5ono2bxmldw36aobt7rep
  libsigsegv@2.10         /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libsigsegv-2.10-cro3222hkjvzqoj4wa7ly2rqf7bisdoc
  libtool@2.4.6           /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libtool-2.4.6-rt7axrxfbcievmeswzvmwfcmdkvrrk4e
  m4@1.4.17               /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/m4-1.4.17-ixzoggem36bu3hjojtd2i3e6wc5gbqyh
  matio@1.5.9             /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/matio-1.5.9-ozit2bfc5bj7nvyoyd42h6ar53kqdyv4
  matio@1.5.9             /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/matio-1.5.9-kdwi6ggu4d6bbb7hawos6gmwdtmev6fz
  metis@5.1.0             /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/metis-5.1.0-hicw2fyxba7mfatl37mcqnpfazkdrrfg
  mpich@3.2               /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mpich-3.2-6zlz4tveokpsolm4c4fb7vybtvlwt7qa
  mumps@5.0.2             /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mumps-5.0.2-andq4bkq5czbzhdwvqafag23zs2v5meg
  mumps@5.0.2             /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mumps-5.0.2-yrl4i6jadjvm6l7vqtt3zvyu4gahyx2h
  ncurses@6.0             /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/ncurses-6.0-ti24btafu5zwhzgzcy5in43e5weafmyr
  netlib-scalapack@2.0.2  /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/netlib-scalapack-2.0.2-7bc2uzwei7unu7pqz32znncp4kkea5ea
  netlib-scalapack@2.0.2  /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/netlib-scalapack-2.0.2-gfj6bxd6z33u52aiv6gxt45bikcdfyfe
  openblas@0.2.19         /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openblas-0.2.19-mm74idshhyfxcnwi3wnubmhg5r6kh4zy
  openmpi@2.0.1           /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openmpi-2.0.1-6vi4ni5z7l4pihbugck6rdylnzuws4ak
  openssl@1.0.2j          /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/openssl-1.0.2j-rtibvnmwjcos263btri3d4lrtucnupa6
  parmetis@4.0.3          /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/parmetis-4.0.3-anb7yswybmszhofapro5avhgsqtc5dbm
  parmetis@4.0.3          /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/parmetis-4.0.3-ueykxwydbhavcg5nlvoecxrl7clz6oby
  suite-sparse@4.5.3      /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/suite-sparse-4.5.3-2udlijaisvewibo6harw3kimhttil2td
  superlu-dist@5.1.1      /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/superlu-dist-5.1.1-asxd3ehyyl3t3fobzzguuh7e24sh2qp4
  superlu-dist@5.1.1      /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/superlu-dist-5.1.1-5c7vjzau6t4xwsg3suzylcp23rpb6a2m
  tbb@2017.3              /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/tbb-2017.3-gsc4orgvu5jnxab6ywcpuxuhwkeztnlc
  trilinos@12.10.1        /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/trilinos-12.10.1-tb3x3fpq564mozkkkcbt4v6bpopi2loz
  util-macros@1.19.0      /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/util-macros-1.19.0-ojeaursjlw3wxrd5dtkkhnovnomej75v
  zlib@1.2.8              /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/zlib-1.2.8-vnwrdo3al6hojzwcf6wf2rr32skvmw45

  -- cray-CNL-haswell / intel@17.0.1.132 --------------------------
  libelf@0.8.13  /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/intel-17.0.1.132/libelf-0.8.13-ununouuxni5psalrxikvscx4wpagpkt

---------------------
Customizing Compilers
---------------------

Spack manages a list of available compilers on the system, detected
automatically from from the user's ``PATH`` variable. The ``spack
compilers`` command is an alias for the command ``spack compiler list``.

.. code-block:: console

  $ spack compilers
  ==> Available compilers
  -- cce ----------------------------------------------------------
  cce@8.5.4  cce@8.5.1  cce@8.5.0  cce@8.4.4  cce@8.4.2  cce@3.210

  -- gcc ----------------------------------------------------------
  gcc@6.2.0  gcc@6.1.0  gcc@5.3.0  gcc@5.2.0  gcc@4.9.3  gcc@4.8

  -- intel --------------------------------------------------------
  intel@17.0.1.132  intel@17.0.0.098  intel@16.0.3.210  intel@16.0.3

The compilers are maintained in a YAML file that can be hand-edited
for special cases. Spack also has tools to add compilers, and
compilers built with Spack can be added to the configuration.

.. code-block:: console

  $ spack install --fake gcc@6.1.0
  ==> Installing gcc
  ==> Installing gmp
  ==> m4 is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/m4-1.4.17-ixzoggem36bu3hjojtd2i3e6wc5gbqyh
  ==> Building gmp [AutotoolsPackage]
  ==> Successfully installed gmp
    Fetch: .  Build: 0.13s.  Total: 0.13s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/gmp-6.1.1-atq5rswc2v66p4dhx43gh63gemurng2z
  ==> Installing isl
  ==> gmp is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/gmp-6.1.1-atq5rswc2v66p4dhx43gh63gemurng2z
  ==> Building isl [Package]
  ==> Successfully installed isl
    Fetch: .  Build: 0.16s.  Total: 0.16s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/isl-0.14-q5srcxmogxm7le44g5qy4k33f27pznsp
  ==> Installing mpc
  ==> gmp is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/gmp-6.1.1-atq5rswc2v66p4dhx43gh63gemurng2z
  ==> Installing mpfr
  ==> gmp is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/gmp-6.1.1-atq5rswc2v66p4dhx43gh63gemurng2z
  ==> Building mpfr [Package]
  ==> Successfully installed mpfr
  Fetch: .  Build: 0.25s.  Total: 0.25s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mpfr-3.1.4-5hf6hjh6zgnchctod2cgwkax3a6eypk7
  ==> Building mpc [Package]
  ==> Successfully installed mpc
  Fetch: .  Build: 0.25s.  Total: 0.25s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mpc-1.0.3-6t5xmm3eiiw2wkm2sv4isppiw5h26pzl
  ==> Installing binutils
  ==> m4 is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/m4-1.4.17-ixzoggem36bu3hjojtd2i3e6wc5gbqyh
  ==> Installing bison
  ==> m4 is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/m4-1.4.17-ixzoggem36bu3hjojtd2i3e6wc5gbqyh
  ==> Building bison [Package]
  ==> Successfully installed bison
  Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/bison-3.0.4-k6ev4apq63sfd5trer7ddt4bvxijlfut
  ==> Installing flex
  ==> bison is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/bison-3.0.4-k6ev4apq63sfd5trer7ddt4bvxijlfut
  ==> Installing gettext
  ==> ncurses is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/ncurses-6.0-ti24btafu5zwhzgzcy5in43e5weafmyr
  ==> Installing libxml2
  ==> Installing xz
  ==> Building xz [Package]
  ==> Successfully installed xz
  Fetch: .  Build: 0.15s.  Total: 0.15s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/xz-5.2.2-za52ojfvaxe2punn6ocgtzgaxpej7yyi
  ==> zlib is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/zlib-1.2.8-vnwrdo3al6hojzwcf6wf2rr32skvmw45
  ==> pkg-config is externally installed in /usr/bin/pkg-config
  ==> Building libxml2 [Package]
  ==> Successfully installed libxml2
  Fetch: .  Build: 0.32s.  Total: 0.32s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/libxml2-2.9.4-ykc2u7wt7ms6msmtsu2jtfjo7vdzozli
  ==> bzip2 is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/bzip2-1.0.6-js6dsfr4ifivstb2bdx6zv5wxddgn3u2
  ==> xz is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/xz-5.2.2-za52ojfvaxe2punn6ocgtzgaxpej7yyi
  ==> Installing tar
  ==> Building tar [AutotoolsPackage]
  ==> Successfully installed tar
  Fetch: .  Build: 0.14s.  Total: 0.14s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/tar-1.29-mqn4poqrh6qqudej3dmlnsbzveninpue
  ==> Building gettext [Package]
  ==> Successfully installed gettext
  Fetch: .  Build: 0.76s.  Total: 0.76s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/gettext-0.19.8.1-7tdvuk44l2iqph6c74i6yparikrtiqy5
  ==> Installing help2man
  ==> gettext is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/gettext-0.19.8.1-7tdvuk44l2iqph6c74i6yparikrtiqy5
  ==> Building help2man [AutotoolsPackage]
  ==> Successfully installed help2man
  Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/help2man-1.47.4-dwxor2gbbcdfldh5c7rnfwpew4y6engu
  ==> Building flex [AutotoolsPackage]
  ==> Successfully installed flex
  Fetch: .  Build: 0.12s.  Total: 0.12s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/flex-2.6.1-kml2cav5kzdzquecy6gzvx2luctsbbdm
  ==> Building binutils [Package]
  ==> Successfully installed binutils
  Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/binutils-2.27-wj4d7cl7hsptqz4hd6cnhpgv4t5bt77p
  ==> mpfr is already installed in /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/mpfr-3.1.4-5hf6hjh6zgnchctod2cgwkax3a6eypk7
  ==> Building gcc [Package]
  ==> Successfully installed gcc
  Fetch: .  Build: 0.65s.  Total: 0.65s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/gcc-6.1.0-ap2f4ijhyrvu4hftz3tth43nouvpsluv


  $ spack find -p gcc
  ==> 1 installed packages.
  -- cray-CNL-haswell / gcc@6.2.0 ---------------------------------
      gcc@6.1.0  /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/gcc-6.1.0-ap2f4ijhyrvu4hftz3tth43nouvpsluv

If we had done a "real" install of gcc, we could add it to our
configuration now using the `spack compiler add` command, but we would
also be waiting for it to install. If we run the command now, it will
return no new compilers.

.. code-block:: console
  $ spack compiler add /global/u2/m/mamelara/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/gcc-6.1.0-ap2f4ijhyrvu4hftz3tth43nouvpsluv
  ==> Found no new compilers

If we had done a real install, the output would have been as follows:

.. code-block:: console

  $ spack compiler add ~/spack/opt/spack/cray-CNL-haswell/gcc-6.2.0/gcc-6.1.0-j5576zbsot2ydljlthjzhsirsesnogvh/bin
  ==> Added 1 new compiler to ~/.spack/cray/compilers.yaml
      gcc@6.1.0

---------------------
Linking External Packages
---------------------

At NERSC, You're likely going to want to link with some of the provided libs
that Cray includes on their systems. In order to do this, Spack has a package
configuration file called ``packages.yaml`` that allows for external software to be
used.

This configuration file is structured like this:

.. code-block:: yaml

  packages:
    package1:
      # settings for package1
    package2:
      # settings for package2
    # ...
    all:
      # setting athat apply to all packages.

To give a more concrete example, this is how someone on a 
Cray will likely set up their packages.yaml file:

.. code-block:: yaml

 packages:
  all:
    compiler: [gcc@6.2.0, intel@17.0.1.132, pgi, clang, xl, nag]
    providers:
      mpi: [openmpi, mpich]
      blas: [openblas]
      lapack: [openblas]
      pil: [py-pillow]
  hdf5:
      buildable: False
      modules:
        hdf5@1.8.16%gcc@6.2.0 arch=cray-CNL-haswell: cray-hdf5/1.8.16
        hdf5@1.8.16%intel@17.0.1.132 arch=cray-CNL-haswell: cray-hdf5/1.8.16
        hdf5@1.8.16%gcc@6.2.0 arch=cray-CNL-mic_knl: cray-hdf5/1.8.16
        hdf5@1.8.16%intel@17.0.1.132 arch=cray-CNL-mic_knl: cray-hdf5/1.8.16
  pkg-config:
      buildable: False
      paths:
          pkg-config@0.28%gcc@6.2.0 arch=cray-CNL-haswell: /usr/bin/pkg-config
          pkg-config@0.28%intel@17.0.1.132 arch=cray-CNL-haswell: /usr/bin/pkg-config
          pkg-config@0.28%gcc@6.2.0 arch=cray-CNL-mic_knl: /usr/bin/pkg-config
          pkg-config@0.28%intel@17.0.1.132 arch=cray-CNL-mic_knl: /usr/bin/pkg-config
  netcdf:
      buildable: False
      modules:
          netcdf@4.4.1%gcc@6.2.0 arch=cray-CNL-haswell: cray-netcdf/4.4.1
          netcdf@4.4.1%intel@17.0.1.132 arch=cray-CNL-haswell: cray-netcdf/4.4.1
          netcdf@4.4.1%gcc@6.2.0 arch=cray-CNL-mic_knl: cray-netcdf/4.4.1
          netcdf@4.4.1%intel@17.0.1.132 arch=cray-CNL-mic_knl: cray-netcdf/4.4.1 

So each package (hdf5, pkg-config, netcdf, etc) will include a full spec and
will either point to a module name or the directory where the package is installed.
For example, with hdf5, we are telling Spack to use the external hdf5 and to
load the cray-hdf5 module when building with this dependency.

So if you want to include cray's own MPI, you will want to add mpich to this
configuration file like using this entry:

.. code-block:: yaml
  mpich:
    buildable: False
    modules:
        mpich@7.4.4%gcc@6.2.0 arch=cray-CNL-haswell: cray-mpich/7.4.4
        mpich@7.4.4%intel@17.0.1.132 arch=cray-CNL-haswell: cray-mpich/7.4.4
        mpich@7.4.4%gcc@6.2.0 arch=cray-CNL-mic_knl: cray-mpich/7.4.4
        mpich@7.4.4%intel@17.0.1.132 arch=cray-CNL-mic_knl: cray-mpich/7.4.4

Go ahead and copy and paste the full entry into ~/.spack/packages.yaml.

.. code-block:: yaml
  packages:
    all:
      compiler: [gcc@6.2.0, intel@17.0.1.132, pgi, clang, xl, nag]
      providers:
        mpi: [openmpi, mpich]
        blas: [openblas]
        lapack: [openblas]
        pil: [py-pillow]
    hdf5:
        modules:
          hdf5@1.8.16%gcc@6.2.0 arch=cray-CNL-haswell: cray-hdf5/1.8.16
          hdf5@1.8.16%intel@17.0.1.132 arch=cray-CNL-haswell: cray-hdf5/1.8.16
          hdf5@1.8.16%gcc@6.2.0 arch=cray-CNL-mic_knl: cray-hdf5/1.8.16
          hdf5@1.8.16%intel@17.0.1.132 arch=cray-CNL-mic_knl: cray-hdf5/1.8.16
    pkg-config:
        buildable: False
        paths:
            pkg-config@0.28%gcc@6.2.0 arch=cray-CNL-haswell: /usr/bin/pkg-config
            pkg-config@0.28%intel@17.0.1.132 arch=cray-CNL-haswell: /usr/bin/pkg-config
            pkg-config@0.28%gcc@6.2.0 arch=cray-CNL-mic_knl: /usr/bin/pkg-config
            pkg-config@0.28%intel@17.0.1.132 arch=cray-CNL-mic_knl: /usr/bin/pkg-config
    netcdf:
        buildable: False
        modules:
            netcdf@4.4.1%gcc@6.2.0 arch=cray-CNL-haswell: cray-netcdf/4.4.1
            netcdf@4.4.1%intel@17.0.1.132 arch=cray-CNL-haswell: cray-netcdf/4.4.1
            netcdf@4.4.1%gcc@6.2.0 arch=cray-CNL-mic_knl: cray-netcdf/4.4.1
            netcdf@4.4.1%intel@17.0.1.132 arch=cray-CNL-mic_knl: cray-netcdf/4.4.1
    mpich:
        buildable: False
        modules:
            mpich@7.4.4%gcc@6.2.0 arch=cray-CNL-haswell: cray-mpich/7.4.4 
            mpich@7.4.4%intel@17.0.1.132 arch=cray-CNL-haswell: cray-mpich/7.4.4
            mpich@7.4.4%gcc@6.2.0 arch=cray-CNL-haswell: cray-mpich/7.4.4
            mpich@7.4.4%intel@17.0.1.132 arch=cray-CNL-haswell: cray-mpich/7.4.4

As of now manually entering external packages is the only way to add entries to
the file. Eventually there will be a command that can sanity check and append 
these entries. There is also work being done to provide Cray platform defaults.
Look for those soon!

------------
Preferred Concretization
------------

Spack can be configured to "prefer" packages/compilers/variants for compiling.
In the concrete example provided, you can prefer the site defaults such as
gcc/6.2.0, and intel/17.0.1.132. You can also prefer your flavor of MPI by
switching mpich to be preferred over openmpi. This will make packages that
depend on mpi to prefer mpich over openmpi and if you have mpich specified
as an external package then Spack will use that external MPI over building
it's own!

.. code-block:: yaml

 packages:
  all:
    compiler: [gcc@6.2.0, intel@17.0.1.132, pgi, clang, xl, nag]
    providers:
      mpi: [mpich, openmpi]
      blas: [openblas]
      lapack: [openblas]
      pil: [py-pillow]

For more information on customizing builds, check out the section on :ref:`build_settings`

-----------
Choosing Targets
-----------
Spack also allows for targets to be chosen in a spec. If you want to build
a package using the new KNL processors, you can specify this using this command.

.. code-block:: console

  $: spack install libelf target=mic_knl

  ==> Installing libelf
  ==> Using cached archive: /global/u2/m/mamelara/spack/var/spack/cache/libelf/libelf-0.8.13.tar.gz
  ==> Staging archive: /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.13-lv2wrtxscaejdtdz5solkftyhdzcdcxu/libelf-0.8.13.tar.gz
  ==> Created stage in /global/u2/m/mamelara/spack/var/spack/stage/libelf-0.8.13-lv2wrtxscaejdtdz5solkftyhdzcdcxu
  ==> Ran patch() for libelf
  ==> Building libelf [AutotoolsPackage]
  ==> Executing phase : 'autoreconf'
  ==> Executing phase : 'configure'
  ==> Executing phase : 'build'
  ==> Executing phase : 'install'
  ==> Successfully installed libelf
    Fetch: 0.01s.  Build: 22.25s.  Total: 22.26s.
  [+] /global/u2/m/mamelara/spack/opt/spack/cray-CNL-mic_knl/gcc-6.2.0/libelf-0.8.13-lv2wrtxscaejdtdz5solkftyhdzcdcxu

This will then load the craype-mic-knl module into your environment.
