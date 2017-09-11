sudo apt-get --assume-yes install build-essential &&
dpkg-reconfigure dash &&
sudo apt-get --assume-yes install libxml-parser-perl open-vm-tools libncurses5-dev gperf makeinfo md5deep &&

git clone https://github.com/OpenELEC/OpenELEC.tv.git

cd OpenELEC.tv

# copy over the metaman distro settings
cp -R ../OpenMediaKraken/distributions/MediaKraken ./distributions/.

# allow it to install packages
PROJECT=Generic DISTRO=MediaKraken ARCH=x86_64 make release
PROJECT=Generic DISTRO=MediaKraken ARCH=x86_64 make image

# general rpi install
PROJECT=RPi DISTRO=MediaKraken ARCH=arm make release
PROJECT=RPi DISTRO=MediaKraken ARCH=arm make image

# general rpi2 install
PROJECT=RPi2 DISTRO=MediaKraken ARCH=arm make release
PROJECT=RPi2 DISTRO=MediaKraken ARCH=arm make image

# general x64 install
PROJECT=Generic ARCH=x86_64 make release
PROJECT=Generic ARCH=x86_64 make image

# general rpi install
PROJECT=RPi ARCH=arm make release
PROJECT=RPi ARCH=arm make image

# general rpi2 install
PROJECT=RPi2 ARCH=arm make release
PROJECT=RPi2 ARCH=arm make image

