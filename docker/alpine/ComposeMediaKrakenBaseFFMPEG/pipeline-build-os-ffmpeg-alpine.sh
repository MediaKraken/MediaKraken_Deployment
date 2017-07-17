#!/bin/bash

mkdir ~/ffmpeg_sources
cd ~/ffmpeg_sources
git clone --depth 1 git://git.videolan.org/x264
cd x264
./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" --enable-static --enable-pic --disable-opencl --disable-asm
make -j16
make install
make distclean

cd ~/ffmpeg_sources
curl -L -O https://get.videolan.org/x265/x265_2.4.tar.gz
tar xzvf x265_2.4.tar.gz
cd ~/ffmpeg_sources/x265_2.4/build/linux
cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_SHARED:bool=off ../../source
make -j16
make install

cd ~/ffmpeg_sources
wget -O fdk-aac.tar.gz https://github.com/mstorsjo/fdk-aac/tarball/master
tar xzvf fdk-aac.tar.gz
cd mstorsjo-fdk-aac*
autoreconf -fiv
./configure --prefix="$HOME/ffmpeg_build" --disable-shared
make -j16
make install
make distclean

#cd ~/ffmpeg_sources
#curl -L -O http://downloads.sourceforge.net/project/lame/lame/3.99/lame-3.99.5.tar.gz
#tar xzvf lame-3.99.5.tar.gz
#cd lame-3.99.5
#./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" --disable-shared --enable-nasm
#make -j16
#make install
#make distclean

#cd ~/ffmpeg_sources
#git clone http://git.opus-codec.org/opus.git
#cd opus
#autoreconf -fiv
#./configure --prefix="$HOME/ffmpeg_build" --disable-shared
#make -j16
#make install
#make distclean

#cd ~/ffmpeg_sources
#curl -O http://downloads.xiph.org/releases/ogg/libogg-1.3.2.tar.gz
#tar xzvf libogg-1.3.2.tar.gz
#cd libogg-1.3.2
#./configure --prefix="$HOME/ffmpeg_build" --disable-shared
#make -j16
#make install
#make distclean

#cd ~/ffmpeg_sources
#curl -O http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.5.tar.gz
#tar xzvf libvorbis-1.3.5.tar.gz
#cd libvorbis-1.3.5
#LDFLAGS="-L$HOME/ffmeg_build/lib" CPPFLAGS="-I$HOME/ffmpeg_build/include" ./configure --prefix="$HOME/ffmpeg_build" --with-ogg="$HOME/ffmpeg_build" --disable-shared
#make -j16
#make install
#make distclean

# alpine is 1.5 while git is 1.6 and includes speed fixes
cd ~/ffmpeg_sources
git clone --depth 1 https://chromium.googlesource.com/webm/libvpx.git
cd libvpx
./configure --prefix="$HOME/ffmpeg_build" --disable-examples --enable-pic --disable-unit-tests
make -j16
make install
make clean

#cd ~/ffmpeg_sources
#curl -L -O http://downloads.xiph.org/releases/speex/speex-1.2rc2.tar.gz
#tar xzvf speex-1.2rc2.tar.gz
#cd speex-1.2rc2
#./configure
#make -j16
#make install

#cd ~/ffmpeg_sources
#curl -L -O http://downloads.xvid.org/downloads/xvidcore-1.3.4.tar.gz
#tar xzvf xvidcore-1.3.4.tar.gz
#cd xvidcore/build/generic
#./configure
#make -j16
#make install

# alpine has 0.13.2
cd ~/ffmpeg_sources
git clone https://github.com/libass/libass.git
#curl -L -O https://github.com/libass/libass/archive/0.13.6.tar.gz
#tar xzvf 0.13.6.tar.gz
#cd libass-0.13.6
cd libass
./autogen.sh
./configure
make -j16
make install

#cd ~/ffmpeg_sources
#curl -L -O http://downloads.xiph.org/releases/theora/libtheora-1.1.1.tar.bz2
#tar xvf libtheora-1.1.1.tar.bz2
#cd libtheora-1.1.1
#./autogen.sh --with-ogg="$HOME/ffmpeg_build" --disable-examples --disable-shared
#make -j16
#make install

cd ~/ffmpeg_sources
curl -L -O https://github.com/MediaKraken/MediaKraken_Submodules/raw/master/xavs.tar.bz2
tar xvf xavs.tar.bz2
cd xavs
./configure
make -j16
make install

#cd ~/ffmpeg_sources
#curl -L -O https://github.com/MediaKraken/MediaKraken_Submodules/raw/master/libmodplug-0.8.8.5.tar.gz
#tar xzvf libmodplug-0.8.8.5.tar.gz
#cd libmodplug-0.8.8.5
#./configure
#make -j16
#make install

cd ~/ffmpeg_sources
curl -L -O https://github.com/MediaKraken-Dependancies/vid.stab/archive/release-0.98b.tar.gz
tar xzvf release-0.98b.tar.gz
cd vid.stab-release-0.98b
cmake .
make
make install

cd ~/ffmpeg_sources
curl -L -O http://downloads.xiph.org/releases/celt/celt-0.11.1.tar.gz
tar xzvf celt-0.11.1.tar.gz
cd celt-0.11.1
./configure --with-ogg="$HOME/ffmpeg_build"
make -j16
make install

cd ~/ffmpeg_sources
curl -L -O https://lib.openmpt.org/files/libopenmpt/src/libopenmpt-0.2.7025-beta20.1.tar.gz
tar xzvf libopenmpt-0.2.7025-beta20.1.tar.gz
cd libopenmpt-0.2.7025
make -j16
make install

cd ~/ffmpeg_sources
git clone https://github.com/Distrotech/libilbc-webrtc.git
cd libilbc-webrtc
./configure
make -j16
make install

#cd ~/ffmpeg_sources
#curl -L -O https://github.com/samba-team/samba/archive/samba-4.5.9.tar.gz
#tar xzvf samba-4.5.9.tar.gz
#cd samba-samba-4.5.9
#./configure --without-acl-support --without-ldap --without-ads
#make -j16
#make install

cd ~/ffmpeg_sources
curl -L -O http://bzip.org/1.0.6/bzip2-1.0.6.tar.gz
tar xzvf bzip2-1.0.6.tar.gz
cd bzip2-1.0.6
make
make install

# skipping for now
#    --enable-decklink \
#    --enable-libgme \
#    --enable-libilbc \
#    --enable-libopencore-amrnb \
#    --enable-libopencore-amrwb \
#    --enable-libpulse \
#    --enable-libschroedinger \
#    --enable-libtwolame \
#    --enable-libv4l2 \
#    --enable-libvidstab \
#    --enable-libxavs \
#    --enable-netcdf \
#    --enable-libdc1394 \
#    --enable-openssl \
#    --enable-libcelt \

cd ~/ffmpeg_sources
# grab the newest only
git clone --depth 1 git://source.ffmpeg.org/ffmpeg
cd ffmpeg
PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
    --prefix="$HOME/ffmpeg_build" \
    --pkg-config-flags="--static" \
    --extra-cflags="-I$HOME/ffmpeg_build/include -I/usr/local/include -I$HOME/ffmpeg_sources/samba-samba-4.5.9/source3/include" \
    --extra-ldflags="-L$HOME/ffmpeg_build/lib -L/usr/local/lib" \
    --bindir="$HOME/bin" \
    --enable-gpl \
    --enable-nonfree \
    --disable-d3d11va \
    --disable-dxva2 \
    --disable-debug \
    --disable-doc \
    --enable-libass \
    --enable-libfdk-aac \
    --enable-libflite \
    --enable-libfontconfig \
    --enable-libfreetype \
    --enable-libfribidi \
    --enable-libgsm \
    --enable-libmodplug \
    --enable-libmp3lame \
    --enable-libopenmpt \
    --enable-libopus \
    --enable-librtmp \
    --enable-libsmbclient \
    --enable-libsnappy \
    --enable-libsoxr \
    --enable-libspeex \
    --enable-libssh \
    --enable-libtheora \
    --enable-libvorbis \
    --enable-libvpx \
    --enable-libwavpack \
    --enable-libx264 \
    --enable-libx265 \
    --enable-libxvid \
    --enable-version3
make -j16
make install
make distclean
hash -r
