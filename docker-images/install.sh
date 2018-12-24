#!/bin/bash -e

echo "======================= Installing gcc 7 ======================"
echo "deb http://ppa.launchpad.net/ubuntu-toolchain-r/test/ubuntu xenial main" >> /etc/apt/sources.list
echo "deb-src http://ppa.launchpad.net/ubuntu-toolchain-r/test/ubuntu xenial main" >> /etc/apt/sources.list
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 60C317803A41BA51845E371A1E9377A2BA9EF27F
apt-get update
# bzip2 is required to install Archiconda3 (miniconda3)
apt-get install -y gcc-7 g++-7 bzip2
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 80 --slave /usr/bin/g++ g++ /usr/bin/g++-7
update-alternatives --install /usr/bin/gcov gcov /usr/bin/gcov-7 80
gcc --version
g++ --version
echo "================== Successfully Installed gcc 7 ==============="

echo "======================== Installing Archiconda3 ==============="
echo yes | /install/Archiconda3-0.1.1-Linux-aarch64.sh -b
export PATH=/root/archiconda3/bin:$PATH
conda update --all --yes
conda install conda-build --yes
conda clean --all --yes
source /root/archiconda3/bin/activate root
conda config --add channels conda-forge
conda config --add channels archiarm
echo "============ Successfully Installed Archiconda3 ==============="

echo "========================= Clean apt-get ========================"
apt-get clean
echo "======================== Cleaned apt-get ======================"
