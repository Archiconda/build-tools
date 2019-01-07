# Archiconda3

This repository holds many configuration scripts for the Archiconda3 distribution.
Focused on porting conda-forge's work to 64 bit Arm processors.


- Shippable: https://app.shippable.com/subs/github/Archiconda/dashboard
- Anaconda: https://anaconda.org/archiarm/
- Github: https://github.com/archiconda/

The goal of this repository is develop the groundwork needed to compile conda-forge on aarch64.
Once that is layed out, we will be working toward backporting much of this work to conda-forge


# Tasks to do:
1. [x] Create an initial Archiconda installer.
2. [x] Upload it to github
3. [x] Create the shippable template that installs the Archiconda installer.
4. [x] Cereate an anaconda channel.
4. [ ] Create the pinnings for Archiconda
5. [x] Create the templates for the different conda-smithy compatible
6. [ ] Figure out how to generate the depency tree for all packages.
7. [x] Start rebuilding a few packages

# How far along the stack do we need to go:

For users to install Archiconda3, they need to be able to install the `conda` package.
`conda-build`, and `anaconda-client` do not need to be in that package, they can be
obtained from `conda-forge` directly.

What this means, is that every package that `conda` depends on, to run, needs to be
an arch specific package. The packages used to build those package do not need to
be arch specific packages.

For now, these are the necessary packages:

  - python-3.7.0-hab5db58_3
  - ca-certificates-2018.11.29-ha4d7672_0
  - conda-env-2.6.0-1
  - libgcc-ng-7.3.0-h5c90dd9_0
  - libstdcxx-ng-7.3.0-h5c90dd9_0
  - libffi-3.2.1-h38784ca_1005
  - ncurses-6.1-hf484d3e_1002
  - openssl-1.0.2p-h14c3975_1002
  - xz-5.2.4-h14c3975_1001
  - yaml-0.1.7-h14c3975_3
  - zlib-1.2.11-h14c3975_1003
  - libedit-3.1.20170329-hf8c457e_1001
  - readline-7.0-h7ce4240_5
  - tk-8.6.8-h14c3975_0
  - sqlite-3.26.0-hf8c457e_1000
  - asn1crypto-0.24.0-py37_1003
  - certifi-2018.11.29-py37_1000
  - chardet-3.0.4-py37_1
  - idna-2.7-py37_0
  - pycosat-0.6.3-py37h14c3975_0
  - pycparser-2.19-py37_0
  - pysocks-1.6.8-py37_0
  - ruamel_yaml-0.15.64-py37h14c3975_0
  - six-1.12.0-py37_1000
  - cffi-1.11.5-py37hb7f436b_1
  - setuptools-40.6.3-py37_0
  - cryptography-2.3.1-py37hb7f436b_1
  - wheel-0.32.3-py37_0
  - pip-18.1-py37_1000
  - pyopenssl-18.0.0-py37_0
  - urllib3-1.23-py37_0
  - requests-2.19.1-py37_0
  - conda-4.5.12-py37_1000


# Limitations of the approach

We are basically compute bound at this point. shippable gives us 1 CI to use at a time (for one organization).

1 build, even for a nearly empty pure python package, takes about 3 minutes.

See for example the package setuptools:
https://app.shippable.com/github/Archiconda/setuptools-feedstock/dashboard

The 3 minutes (180 seconds) are broken up as follows:

- 15s Shippable things we have no control over
- 5 seconds updating ubuntu's cache of apt
- 4 seconds installing bzip2 and curl
- 2 seconds downloading Archiconda3
- 40 seconds installing Archiconda3 (including conda-build and anaconda-client)
- 100 seconds building the package
- 5 seconds getting the package name
- 5 seconds to upload the package
- 1 second leaning up.

We can maybe cut 50 seconds of this by uploading our own container.

But ultimately, we only have 1 CI, with 1 parallel job at a time, so we cannot run too many
feedstocks at once.

It does have 96 cores, so maybe we can find a different way to parallelize things? I really feel
like that might be over complicating things.

# How to speed things up

I haven't had many problems compiling standard software.

For example, python compiled on the first shot, and the issues were primarely due to the fact
that some software hardcodes binutil dependencies.

Therefore, we can potentially not have shippable automatically get triggered.

Users would have to wait until a regular linux 64 bit build passes, before triggering the shippable
build.


# How to start:

## Be friends with jjhelmus

He will build the following critial packages:

The compilers and libstdc

These include the following:

```
binutils_impl_linux-aarch64-2.29.1-hc862510_0.tar.bz2
binutils_linux-aarch64-2.29.1-h1dbaa89_0.tar.bz2
crosstool-ng-1.23.0.451_g5888cf1-5.tar.bz2
gcc_impl_linux-aarch64-7.3.0-h68995b2_0.tar.bz2
gcc_linux-aarch64-7.3.0-h98564e2_0.tar.bz2
gdb_linux-aarch64-7.12.1-h6bc79d0_0.tar.bz2
gfortran_impl_linux-aarch64-7.3.0-h5c90dd9_0.tar.bz2
gfortran_linux-aarch64-7.3.0-h98564e2_0.tar.bz2
gxx_impl_linux-aarch64-7.3.0-h5c90dd9_0.tar.bz2
gxx_linux-aarch64-7.3.0-h98564e2_0.tar.bz2
libgcc-ng-7.3.0-h5c90dd9_0.tar.bz2
libgfortran-ng-7.3.0-h6bc79d0_0.tar.bz2
libstdcxx-ng-7.3.0-h5c90dd9_0.tar.bz2
```

Technically you don't need make (listed below), but i've had so much trouble building it,
I'm just going to take jjhelmus'

```
make-4.2.1-h7b6447c_1.tar.bz2
```

These packages are available from his [c4aarch64 anaconda channel](https://anaconda.org/c4aarch64/).


He also created a tag on anaconda.org, I assume through cross compilation,
where you can bootstrap a conda for aarch64.

```
https://anaconda.org/jjhelmus/repo?label=aarch64_bootstrap
```

# Now the fun stuff

1. Create a docker image that uses Centos7, and has Archiconda installed.

2. There is a bug in the version of conda in the bootstrap, that doesn't allow you to have multiple channels.
The maximum number of channels is 2. This is why this next step is important.

3. Use that anaconda channel to create an anaconda installer. See the `installer` directory
in this repositiory.

4. Start building pacakges.

5. You can try and build make, but after you do that, try and build m4 with your newly cut version of make.
I couldn't get it to work. I think jjhelmus did something special. Or I did something wrong :/

6. The build order is documented https://github.com/Archiconda/build-tools/issues/4

## Building recipes

Most of the heavy lifting is done by `fork_conda_forge.py`, a python script that does:

1. Uses the github API to check if Archiconda already has the desired feedstock.
2. If not, it will fork it from conda-forge
3. Sets up an aarch64 branch.
4. Enables building the repository on shippable.
    * To enable the repository on shippable, you must first request access to aarch64 machines.
    * Once you get access, you need ~~to pay for an API key~~ ~~trust that I'm not stealing your creditials~~, inspect the code in `fork_conda_forge.py` to believe that I'm not stealing your credentials.
    * You will see a chrome window popup, and some explination on the command line as to what is happening.
    * Basically, I screen scrape and click buttons for you to enable the repository.
    * You need to log in manually the first time so that the script can save your cookies.
5. Rerenders the recipe with `conda smithy rerender`
    * You should install conda-smithy from `Archiconda` to rerender things correctly.
6. Pushes the changes to the `aarch64` branch.

Because the repository has been enabled, pushing to that branch will trigger a build on shippable.

## Docker image

The Docker image should:

1. Set the locale

```
# Set the locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
```

2. Install a few basic pacakges. `bzip2` and `curl` or `wget` are necessary to help bootstrap the process.

3. Install Archiconda3.

4. Add the archiconda3 to the path.


### aarch64 docker on x86 using qemu

If you are creating the docker image while running on your personal laptop, it is useful to
use `qemu-static` to run an `aarch64` inside `x86`.

Put the line
```
# needed to build this on x86
COPY qemu-aarch64-static /usr/bin/
```

and you should be gravy.


### Bulding using qemu and docker

I've found that it can be helpful to build and test using qemu and docker.
It might be as simple as iterating quickly to find what dependencies were missing from
the original packages.

Often, binutils are hardcoded, so you have to pass compilation flags to tell the build
system what `ar` command to use.

It might be useful to mount a local directory to use with the docker build system.

For example, the following command mounts the registration directory which
contains a bunch of feedstocks and runs the `archiconda/centos7` image.
The first command it runs is `bash` allows you to interact with the system.

```
docker run -v /home/mark2/git/aarch64/build-tools/registration:/feedstocks -i -t archiconda/centos7 bash
```

Be warned, CPU emulation is SLOW and will make your computer crawl.

I started compiling `cmake` at the same time it did on shippable, and didn't even get through the
bootstrap when it has finished compiling.

