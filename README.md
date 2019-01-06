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

