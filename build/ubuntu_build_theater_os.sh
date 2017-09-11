sudo apt-get --assume-yes install build-essential &&
dpkg-reconfigure dash &&
sudo apt-get --assume-yes install libxml-parser-perl open-vm-tools libncurses5-dev gperf makeinfo md5deep &&

git clone https://github.com/LibreELEC/LibreELEC.tv.git

# copy over the mediakraken distro settings
cp -R ./OpenMediaKraken/distributions/MediaKraken ./LibreELEC.tv/distributions/.

cd LibreELEC.tv

# allow it to install packages
PROJECT=Generic DISTRO=MediaKraken ARCH=x86_64 make -j20 release
PROJECT=Generic DISTRO=MediaKraken ARCH=x86_64 make -j20 image

# general rpi install
PROJECT=RPi DISTRO=MediaKraken ARCH=arm make -j20 release
PROJECT=RPi DISTRO=MediaKraken ARCH=arm make -j20 image

# general rpi2 install
PROJECT=RPi2 DISTRO=MediaKraken ARCH=arm make -j20 release
PROJECT=RPi2 DISTRO=MediaKraken ARCH=arm make -j20 image

# general x64 install
PROJECT=Generic ARCH=x86_64 make -j20 release
PROJECT=Generic ARCH=x86_64 make -j20 image

# general rpi install
PROJECT=RPi ARCH=arm make -j20 release
PROJECT=RPi ARCH=arm make -j20 image

# general rpi2 install
PROJECT=RPi2 ARCH=arm make -j20 release
PROJECT=RPi2 ARCH=arm make -j20 image

