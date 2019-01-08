#!/bin/bash -e

echo "======================= Installing gcc 7 ======================"
#echo "deb http://ppa.launchpad.net/ubuntu-toolchain-r/test/ubuntu xenial main" >> /etc/apt/sources.list
#echo "deb-src http://ppa.launchpad.net/ubuntu-toolchain-r/test/ubuntu xenial main" >> /etc/apt/sources.list
# bzip2 is required to install Archiconda3 (miniconda3)
# curl jq and git are required for shippable to work without delay
apt-get update
apt-get install -y bzip2 curl jq git locales vim
locale-gen en_US.UTF-8
echo "================== Successfully Installed gcc 7 ==============="

echo "======================== Installing Archiconda3 ==============="
echo yes | /install/Archiconda3-0.2.0-Linux-aarch64.sh -b
export PATH=/root/archiconda3/bin:$PATH
conda update --all --yes
#conda install anaconda-client conda-build --yes
conda clean --all --yes
source /root/archiconda3/bin/activate root
echo "============ Successfully Installed Archiconda3 ==============="

echo "========================= Clean apt-get ========================"
apt-get clean
echo "======================== Cleaned apt-get ======================"
