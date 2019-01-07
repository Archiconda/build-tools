FROM arm64v8/ubuntu:18.04
# See for how to use qemu
# https://ownyourbits.com/2018/06/27/running-and-building-arm-docker-containers-in-x86/

# needed to build this on x86
COPY qemu-aarch64-static /usr/bin/


# These dependencies are necessary to bootstrap conda
# these help build crosstools-ng
#RUN apt-get update && 
#RUN apt-get install -y g++ gperf texinfo help2man automake gawk make libncursesw5-dev wget
# For some reason crosstools-ng wants ncursesw to be located there
# So just put it there.
#RUN ln -s /usr/include/ncursesw /usr/include/ncurses

RUN export PATH=/root/archiconda3/bin:$PATH

ADD . /install
RUN /install/install.sh
# Can this go in the install script?

# Do we need to remove this?
#RUN rm /usr/bin/qemu-aarch64-static
