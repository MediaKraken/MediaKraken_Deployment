#!/bin/bash
apk add sdl-dev fontconfig-dev alsa-lib-dev qt5-qtbase-dev
cd /var/lib/jenkins/workspace/MediaKraken-PyLint/MediaKraken_Build/lib/
unzip mame0176s.zip
mkdir tmp
mv mame.zip tmp/.
cd tmp
unzip mame.zip
make -j4 TARGET=ume
make -j4 SUBTARGET=mess
make -j4
