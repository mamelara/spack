.. _feature_overview:

======================
Feature Overview
======================

This page serves as a quick highlight of all the different features and 
configurations that are available to you in spack. 

.. _feature_overview-scope:
------------------
Scope
------------------

There are different scopes of configuration files available in Spack. Here they
are from lowest to highest:

1. **defaults**: Found in ``$(prefix)/etc/spack/defaults/``. Factory settings
   that should generally not be modified but instead overridden.

2. **site**: Found in ``$(prefix)/etc/spack/``. Only affects *this instance* of
   Spack. Site is used per project or for site-wide or multi-user machine. 
   Use case is usually for a common spack instance across machines.

3. **user**: Stored in the home directory: ``~/.spack/``. These settings affect
   all instances of Spack and take highest precedence.

-------------------
Example
-------------------

As as an example let's go ahead and look at our different configurations. 
Spack has it's own command to look at different config files. ``spack config get [config_name]``.

The different config files available to you are: 

- **compilers** 
- **config** 
- **mirrors** 
- **modules** 
- **packages** 
- **repos**

Let's look at what is inside of the compilers.yaml file:

.. code-block:: console
  
  $ spack config get compilers
  compilers:
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules:
      - PrgEnv-cray
      - cce/8.4.2
      operating_system: CNL
      paths:
        cc: cc
        cxx: CC
        f77: ftn
        fc: ftn
      spec: cce@8.4.2
      target: any
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules:
      - PrgEnv-cray
      - cce/8.5.0
      operating_system: CNL
      paths:
        cc: cc
        cxx: CC
        f77: ftn
        fc: ftn
      spec: cce@8.5.0
      target: any
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules:
      - PrgEnv-cray
      - cce/8.5.4
      operating_system: CNL
      paths:
        cc: cc
        cxx: CC
        f77: ftn
        fc: ftn
      spec: cce@8.5.4
      target: any
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules:
      - PrgEnv-cray
      - cce/8.4.4
      operating_system: CNL
      paths:
        cc: cc
        cxx: CC
        f77: ftn
        fc: ftn
      spec: cce@8.4.4
      target: any
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules:
      - PrgEnv-cray
      - cce/8.5.1
      operating_system: CNL
      paths:
        cc: cc
        cxx: CC
        f77: ftn
        fc: ftn
      spec: cce@8.5.1
      target: any
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules:
      - PrgEnv-gnu
      - gcc/4.9.3
      operating_system: CNL
      paths:
        cc: cc
        cxx: CC
        f77: ftn
        fc: ftn
      spec: gcc@4.9.3
      target: any
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules:
      - PrgEnv-gnu
      - gcc/5.3.0
      operating_system: CNL
      paths:
        cc: cc
        cxx: CC
        f77: ftn
        fc: ftn
      spec: gcc@5.3.0
      target: any
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules:
      - PrgEnv-gnu
      - gcc/6.2.0
      operating_system: CNL
      paths:
        cc: cc
        cxx: CC
        f77: ftn
        fc: ftn
      spec: gcc@6.2.0
      target: any
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules:
      - PrgEnv-gnu
      - gcc/5.2.0
      operating_system: CNL
      paths:
        cc: cc
        cxx: CC
        f77: ftn
        fc: ftn
      spec: gcc@5.2.0
      target: any
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules:
      - PrgEnv-gnu
      - gcc/6.1.0
      operating_system: CNL
      paths:
        cc: cc
        cxx: CC
        f77: ftn
        fc: ftn
      spec: gcc@6.1.0
      target: any
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules:
      - PrgEnv-intel
      - intel/16.0.3.210
      operating_system: CNL
      paths:
        cc: cc
        cxx: CC
        f77: ftn
        fc: ftn
      spec: intel@16.0.3.210
      target: any
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules:
      - PrgEnv-intel
      - intel/17.0.0.098
      operating_system: CNL
      paths:
        cc: cc
        cxx: CC
        f77: ftn
        fc: ftn
      spec: intel@17.0.0.098
      target: any
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules:
      - PrgEnv-intel
      - intel/17.0.1.132
      operating_system: CNL
      paths:
        cc: cc
        cxx: CC
        f77: ftn
        fc: ftn
      spec: intel@17.0.1.132
      target: any
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules: []
      operating_system: sles12
      paths:
        cc: /opt/cray/pe/craype/2.5.7/bin/cc
        cxx: /opt/cray/pe/craype/2.5.7/bin/CC
        f77: /opt/cray/pe/craype/2.5.7/bin/ftn
        fc: /opt/cray/pe/craype/2.5.7/bin/ftn
      spec: cce@3.210
      target: x86_64
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules: []
      operating_system: sles12
      paths:
        cc: /usr/bin/gcc-4.8
        cxx: /usr/bin/g++-4.8
        f77: null
        fc: null
      spec: gcc@4.8
      target: x86_64
  - compiler:
      environment: {}
      extra_rpaths: []
      flags: {}
      modules: []
      operating_system: sles12
      paths:
        cc: /opt/intel/compilers_and_libraries_2016.3.210/linux/bin/intel64/icc
        cxx: /opt/intel/compilers_and_libraries_2016.3.210/linux/bin/intel64/icpc
        f77: /opt/intel/compilers_and_libraries_2016.3.210/linux/bin/intel64/ifort
        fc: /opt/intel/compilers_and_libraries_2016.3.210/linux/bin/intel64/ifort
      spec: intel@16.0.3
      target: x86_64

You might have been asking yourself how does Spack call compilers, specifically
how does Spack call Cray's own compiler wrappers? The key to the answer is that
when you run an instance of spack without a compilers.yaml file, then Spack will
parse through your $PATH variable and find compilers there, and it will also 
look through environment modules through ``modulecmd python avail [comp-name]``.

From there Spack's own compiler wrappers then execute the compiler binary,
which in the case of Cray compilers is cc, CC and ftn.

----------------
Config.yaml
---------------

With config.yaml, you can change some of the behavior of Spack. This includes
changing the location of the install tree for packages, the location where
Spack places modulefiles, and the temp build directories.

Defaults are these:

.. code-block:: console 
  $ spack config get config
  config:
    build_stage:
    - $tempdir
    - /nfs/tmp2/$user
    - $spack/var/spack/stage
    checksum: true
    dirty: false
    install_tree: $spack/opt/spack
    misc_cache: ~/.spack/cache
    module_roots:
      dotkit: $spack/share/spack/dotkit
      lmod: $spack/share/spack/lmod
      tcl: $spack/share/spack/modules
    source_cache: $spack/var/spack/cache
    verify_ssl: true

Let's try to change where spack installs packages:

.. code-block:: console
  
  $ spack config edit config


Your editor should have opened an empty file. This is because we only have our
defaults set, and when we run the command spack config edit, Spack will default
to the scope with the highest precedence (~/.spack). Lets add to this file:

.. code-block:: yaml
  
   config:
    install_tree: /global/homes/m/mamelara/nersc-packages


Then if we install libelf

.. code-block:: console
    
  $ spack install libelf
    ....

and then look at the directory we specified, we will see that spack has created
the directory and placed the install tree into it.

Let's see what our config looks like now:

.. code-block:: console 
  config:
    build_stage:
    - $tempdir
    - /nfs/tmp2/$user
    - $spack/var/spack/stage
    checksum: true
    dirty: false
    install_tree: /global/homes/m/mamelara/nersc_packages
    misc_cache: ~/.spack/cache
    module_roots:
      dotkit: $spack/share/spack/dotkit
      lmod: $spack/share/spack/lmod
      tcl: $spack/share/spack/modules
    source_cache: $spack/var/spack/cache
    verify_ssl: true

install_tree has changed but the rest has not. This is because spack overrides
single settings when they are declared in other scopes. In order to fully
override a scope you need to replace ``config:`` with  ``config::``.

###########################
Customizing Builds
###########################

We briefly talked about using external packages during our tutorial of basic
usage. This is all done using a packages.yaml configuration file. As a review,
all that is needed to use an external package is a spec that is as fully
concretized as possible (i.e a spec with a package version, a compiler and 
compiler version, and an architecture) and a module name or path to the
installed package.

-----------------------
Preferred Concretization
-----------------------

You can declare certain packages and compilers to be preferred when building
than other options. For example let's take a look at our packages.yaml file
located in ``$SPACK_ROOT/etc/spack/packages.yaml``.

.. code-block:: yaml
  packages:
    all:
      compiler: [gcc@6.2.0, intel@17.0.1.132, pgi, clang, xl, nag]
      providers:
        mpi: [mpich, openmpi]
        blas: [openblas]
        lapack: [openblas]
        pil: [py-pillow]

We currently have gcc-6.2.0 to be the preferred compiler for gcc and 
intel-17.0.1.132 to be the preferred compiler for intel. We also have the order set to have
the gcc compiler to be the default compiler when no compiler is specified
through the spec.

We can confirm this by using the ``spack spec <package_name>`` command:

.. code-block:: console
  $ spack spec zlib
  Input spec
  --------------------------------
  zlib

  Normalized
  --------------------------------
  zlib

  Concretized
  --------------------------------
  zlib@1.2.8%gcc@6.2.0+pic arch=cray-CNL-haswell

If we switch the order around and put ``intel@17.0.1.132`` as our default and
subsequently provide a spec, Spack will concretize using our intel compiler.

.. code-block:: console
  $ spack spec zlib
  Input spec
  --------------------------------
  zlib

  Normalized
  --------------------------------
  zlib

  Concretized
  --------------------------------
  zlib@1.2.8%intel@17.0.1.132+pic arch=cray-CNL-haswell
