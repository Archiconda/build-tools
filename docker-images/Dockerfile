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
  && yum clean all

ENV PATH="/root/archiconda3/bin:${PATH}"
COPY Archiconda3Builder-0.1.2-Linux-aarch64.sh /.
RUN sh /Archiconda3Builder-0.1.2-Linux-aarch64.sh -b -p /root/archiconda3
