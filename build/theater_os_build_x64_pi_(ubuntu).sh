sudo dpkg-reconfigure dash

CODEVERSION=7.0.3

wget https://github.com/LibreELEC/LibreELEC.tv/archive/$CODEVERSION.zip
unzip $CODEVERSION.zip
cd LibreELEC.tv-$CODEVERSION

#git clone https://github.com/LibreELEC/LibreELEC.tv.git
#cd LibreELEC.tv
#git checkout libreelec-8.2

# copy over the mediakraken distro settings
cp -R ../OpenMediaKraken/distributions/MediaKraken ./distributions/.

# allow it to install packages
PROJECT=Generic DISTRO=MediaKraken ARCH=x86_64 make -j20 release
PROJECT=Generic DISTRO=MediaKraken ARCH=x86_64 make -j20 image

# general rpi and pi zero install
PROJECT=RPi DISTRO=MediaKraken ARCH=arm make -j20 release
PROJECT=RPi DISTRO=MediaKraken ARCH=arm make -j20 image

# general rpi2 install
PROJECT=RPi2 DISTRO=MediaKraken ARCH=arm make -j20 release
PROJECT=RPi2 DISTRO=MediaKraken ARCH=arm make -j20 image
