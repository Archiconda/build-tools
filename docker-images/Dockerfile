FROM arm64v8/centos:7

# needed to build this on x86
COPY qemu-aarch64-static /usr/bin/

# Set the locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# base packages
RUN yum install -y \
  file \
  libX11 \
  libX11-devel \
  libXau \
  libxcb \
  libXdmcp \
  libXext \
  libXrender \
  libXt \
  mesa-libGL \
  mesa-libGLU \
  openssh-clients \
  patch \
  rsync \
  util-linux \
  wget \
  which \
  bzip2 \
  xorg-x11-server-Xvfb \
  git \
  && yum clean all

# sudo is necessary for shippable to boot up the container
# git seems to be necessary to pull in the source
RUN yum install -y \
  sudo \
  git \
  && yum clean all

# Remove the centos binutils tools so that we make sure we arn't using them accidentally
# You can't remove these with yum because apparently it would delete the whole system.
# RUN bash -c "rm -f /usr/bin/{ar,addr2line,as,c++filt,dwp,elfedit,gprof,ld,ld.bfd,ld.gold,nm,objcopy,objdump,ranlib,readlef,size,strings,strip}"


ENV PATH="/root/archiconda3/bin:${PATH}"
#COPY Archiconda3Builder-0.1.2-Linux-aarch64.sh /.
#RUN sh /Archiconda3Builder-0.1.2-Linux-aarch64.sh -b -p /root/archiconda3
COPY Archiconda3-0.2.3-Linux-aarch64.sh /.
RUN sh /Archiconda3-0.2.3-Linux-aarch64.sh -b -p /root/archiconda3
RUN rm Archiconda3-0.2.3-Linux-aarch64.sh

ENV PATH="/root/archiconda3/bin:${PATH}"
RUN conda config --add channels conda-forge
RUN conda config --add channels c4aarch64
RUN conda install conda-build
RUN conda install anaconda-client


