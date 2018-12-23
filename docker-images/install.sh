#!/bin/bash -e

echo "========================= Clean apt-get ========================"
apt-get clean
mv /var/lib/apt/lists/* /tmp
mkdir -p /var/lib/apt/lists/partial
apt-get clean
apt-get update
echo "======================== Cleaned apt-get ======================"

echo "======================== Installing Archiconda3 ==============="
apt-get install -y bzip2
echo yes | /install/Archiconda3-0.1.1-Linux-aarch64.sh -b
echo "============ Successfully Installed Archiconda3 ==============="


echo "======================= Installing gcc 7 ======================"
# Man I really don't like installing all these dependencies,
# but for some reason, it seemed like I had to to get the arm repos???
apt-get install -y software-properties-common
# echo "deb http://ppa.launchpad.net/ubuntu-toolchain-r/test/ubuntu xenial main" >> /etc/apt/source.list
# echo "deb-src http://ppa.launchpad.net/ubuntu-toolchain-r/test/ubuntu xenial main" >> /etc/apt/source.list
# apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 60C317803A41BA51845E371A1E9377A2BA9EF27F
add-apt-repository ppa:ubuntu-toolchain-r/test
apt-get update
apt-get update
apt-get install -y gcc-7 g++-7
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 80 --slave /usr/bin/g++ g++ /usr/bin/g++-7
update-alternatives --install /usr/bin/gcov gcov /usr/bin/gcov-7 80
gcc --version
g++ --version
echo "================== Successfully Installed gcc 7 ==============="
