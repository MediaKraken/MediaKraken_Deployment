#!/bin/bash

mkdir ~/ffmpeg_sources

# need newer version to compile x264
cd ~/ffmpeg_sources
curl -L -O http://www.nasm.us/pub/nasm/releasebuilds/2.13.01/nasm-2.13.01.tar.gz
tar xzvf nasm-2.13.01.tar.gz
cd nasm-2.13.01
./configure
make -j16
make install

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
#./configure --prefix="$HOME/ffmpeg_build"
#make -j8
#make install
#make distclean

# unbuntu only has 1.3.1
cd ~/ffmpeg_sources
curl -O http://downloads.xiph.org/releases/ogg/libogg-1.3.2.tar.gz
tar xzvf libogg-1.3.2.tar.gz
cd libogg-1.3.2
./configure --prefix="$HOME/ffmpeg_build" --disable-shared
make -j16
make install
make distclean

#cd ~/ffmpeg_sources
#curl -O http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.4.tar.gz
#tar xzvf libvorbis-1.3.4.tar.gz
#cd libvorbis-1.3.4
#LDFLAGS="-L$HOME/ffmeg_build/lib" CPPFLAGS="-I$HOME/ffmpeg_build/include" ./configure --prefix="$HOME/ffmpeg_build" --with-#ogg="$HOME/ffmpeg_build" --disable-shared
#make -j16
#make install
#make distclean

#cd ~/ffmpeg_sources
#git clone --depth 1 https://chromium.googlesource.com/webm/libvpx.git
#cd libvpx
#./configure --prefix="$HOME/ffmpeg_build" --disable-examples
#make -j8
#make install
#make clean

cd ~/ffmpeg_sources
wget downloads.xiph.org/releases/celt/celt-0.11.1.tar.gz
tar xzvf celt-0.11.1.tar.gz
cd celt-0.11.1
./configure
make -j16
make install

# skipping for now
#    --enable-decklink \
#    --enable-libgme \
#    --enable-libilbc \
#    --enable-libpulse \
#    --enable-libschroedinger \
#    --enable-libtwolame \
#    --enable-libv4l2 \
#    --enable-libvidstab \
#    --enable-libxavs \
#    --enable-netcdf \
#    --enable-libdc1394 \
#    --enable-openssl \
#    --enable-libopenmpt \
#    --enable-libssh \

cd ~/ffmpeg_sources
# grab the newest only
git clone --depth 1 git://source.ffmpeg.org/ffmpeg
cd ffmpeg
PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
    --prefix="$HOME/ffmpeg_build" \
    --pkg-config-flags="--static" \
    --extra-cflags="-I/usr/local/cuda/include -I$HOME/ffmpeg_build/include -I/usr/local/include" \
    --extra-ldflags="-L$HOME/ffmpeg_build/lib -L/usr/local/lib -L/usr/local/cuda/lib64" \
    --bindir="$HOME/bin" \
    --enable-gpl \
    --enable-nonfree \
    --disable-d3d11va \
    --disable-dxva2 \
    --disable-debug \
    --disable-doc \
    --enable-libass \
    --enable-libcelt \
    --enable-libopencore-amrnb \
    --enable-libopencore-amrwb \
    --enable-libfdk-aac \
    --enable-libflite \
    --enable-libfontconfig \
    --enable-libfreetype \
    --enable-libfribidi \
    --enable-libgsm \
    --enable-libmodplug \
    --enable-libmp3lame \
    --enable-libopus \
    --enable-librtmp \
    --enable-libsmbclient \
    --enable-libsnappy \
    --enable-libsoxr \
    --enable-libspeex \
    --enable-libtheora \
    --enable-libvorbis \
    --enable-libvpx \
    --enable-libwavpack \
    --enable-libx264 \
    --enable-libx265 \
    --enable-libxvid \
    --enable-cuda \
    --enable-cuvid \
    --enable-nvenc \
    --enable-libnpp \
    --enable-version3
make -j16
make install
make distclean
hash -r
