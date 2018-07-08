sudo dpkg-reconfigure dash

CODEVERSION=8.1.1

# check to see if it's already been fetched
if [ ! -f "$CODEVERSION.zip" ]
then
    wget get https://github.com/LibreELEC/LibreELEC.tv/archive/$CODEVERSION.zip
    unzip $CODEVERSION.zip
fi

# enter le folder
cd LibreELEC.tv-$CODEVERSION

# copy over the mediakraken distro settings
cp -R ./OpenMediaKraken/distributions/MediaKraken ./distributions/.
cp -R ./OpenMediaKraken/packages/* ./packages/.

# allow it to install packages
PROJECT=Generic DISTRO=MediaKraken ARCH=x86_64 make -j`getconf _NPROCESSORS_ONLN` release
PROJECT=Generic DISTRO=MediaKraken ARCH=x86_64 make -j`getconf _NPROCESSORS_ONLN` image

# general rpi and pi zero install
PROJECT=RPi DISTRO=MediaKraken ARCH=arm make -j`getconf _NPROCESSORS_ONLN` release
PROJECT=RPi DISTRO=MediaKraken ARCH=arm make -j`getconf _NPROCESSORS_ONLN` image

# general rpi2 install
PROJECT=RPi2 DISTRO=MediaKraken ARCH=arm make -j`getconf _NPROCESSORS_ONLN` release
PROJECT=RPi2 DISTRO=MediaKraken ARCH=arm make -j`getconf _NPROCESSORS_ONLN` image
