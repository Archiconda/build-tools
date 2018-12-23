FROM arm64v8/ubuntu:16.04
# See for how to use qemu
# https://ownyourbits.com/2018/06/27/running-and-building-arm-docker-containers-in-x86/

# needed to build this on x86
COPY qemu-aarch64-static /usr/bin/

ADD . /install
RUN /install/install.sh
# Can this go in the install script?
RUN export PATH=/root/archiconda3/bin:$PATH

# Do we need to remove this?
RUN rm /usr/bin/qemu-aarch64-static
