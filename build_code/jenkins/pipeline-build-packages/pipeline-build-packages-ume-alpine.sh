#!/bin/bash
apk add sdl-dev fontconfig-dev alsa-lib-dev qt5-qtbase-dev
wget https://github.com/mamedev/mame/releases/download/mame0181/mame0181s.zip
unzip mame0181s.zip
mkdir tmp
mv mame.zip tmp/.
cd tmp
unzip mame.zip
make -j12
