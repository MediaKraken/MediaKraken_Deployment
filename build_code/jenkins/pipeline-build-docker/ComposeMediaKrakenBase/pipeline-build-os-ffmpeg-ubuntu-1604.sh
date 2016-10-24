#!/bin/bash
#https://github.com/FFmpeg/FFmpeg/blob/master/configure

mkdir ~/ffmpeg_sources

cd ~/ffmpeg_sources
git clone git://github.com/yasm/yasm.git
cd yasm
./autogen.sh
./configure
make -j8
make install

cd ~/ffmpeg_sources
git clone --depth 1 git://git.videolan.org/x264
cd x264
./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" --enable-static --disable-opencl
make -j8
make install
make distclean

cd ~/ffmpeg_sources
curl -L -O https://get.videolan.org/x265/x265_2.1.tar.gz
tar xzvf x265_2.1.tar.gz
cd ~/ffmpeg_sources/x265_2.1/build/linux
cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_SHARED:bool=off ../../source
make -j8
make install

cd ~/ffmpeg_sources
wget -O fdk-aac.tar.gz https://github.com/mstorsjo/fdk-aac/tarball/master
tar xzvf fdk-aac.tar.gz
cd mstorsjo-fdk-aac*
autoreconf -fiv
./configure --prefix="$HOME/ffmpeg_build" --disable-shared
make -j8
make install
make distclean

cd ~/ffmpeg_sources
curl -L -O http://downloads.sourceforge.net/project/lame/lame/3.99/lame-3.99.5.tar.gz
tar xzvf lame-3.99.5.tar.gz
cd lame-3.99.5
./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" --disable-shared --enable-nasm
make -j8
make install
make distclean

cd ~/ffmpeg_sources
git clone http://git.opus-codec.org/opus.git
cd opus
autoreconf -fiv
./configure --prefix="$HOME/ffmpeg_build" --disable-shared
make -j8
make install
make distclean

cd ~/ffmpeg_sources
curl -L -O http://downloads.xiph.org/releases/ogg/libogg-1.3.2.tar.gz
tar xzvf libogg-1.3.2.tar.gz
cd libogg-1.3.2
./configure --prefix="$HOME/ffmpeg_build" --disable-shared
make -j8
make install
make distclean

cd ~/ffmpeg_sources
curl -L -O http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.5.tar.gz
tar xzvf libvorbis-1.3.5.tar.gz
cd libvorbis-1.3.5
LDFLAGS="-L$HOME/ffmeg_build/lib" CPPFLAGS="-I$HOME/ffmpeg_build/include" ./configure --prefix="$HOME/ffmpeg_build" --with-ogg="$HOME/ffmpeg_build" --disable-shared
make -j8
make install
make distclean

cd ~/ffmpeg_sources
git clone --depth 1 https://chromium.googlesource.com/webm/libvpx.git
cd libvpx
./configure --prefix="$HOME/ffmpeg_build" --disable-examples --disable-unit-tests
make -j8
make install
make clean

cd ~/ffmpeg_sources
curl -L -O http://downloads.xiph.org/releases/speex/speex-1.2rc2.tar.gz
tar xzvf speex-1.2rc2.tar.gz
cd speex-1.2rc2
./configure
make -j8
make install

cd ~/ffmpeg_sources
curl -L -O http://downloads.xvid.org/downloads/xvidcore-1.3.4.tar.gz
tar xzvf xvidcore-1.3.4.tar.gz
cd xvidcore/build/generic
./configure
make -j8
make install

cd ~/ffmpeg_sources
curl -L -O https://github.com/libass/libass/archive/0.13.4.tar.gz
tar xzvf 0.13.4.tar.gz
cd libass-0.13.4
./autogen.sh
./configure
make -j8
make install

cd ~/ffmpeg_sources
curl -L -O http://downloads.xiph.org/releases/theora/libtheora-1.1.1.tar.bz2
tar xvf libtheora-1.1.1.tar.bz2
cd libtheora-1.1.1
./autogen.sh --with-ogg="$HOME/ffmpeg_build" --disable-examples --disable-shared
make -j8
make install

cd ~/ffmpeg_sources
curl -L -O https://github.com/MediaKraken/MediaKraken_Submodules/raw/master/xavs.tar.bz2
tar xvf xavs.tar.bz2
cd xavs
./configure
make -j8
make install

cd ~/ffmpeg_sources
curl -L -O https://github.com/MediaKraken/MediaKraken_Submodules/raw/master/libmodplug-0.8.8.5.tar.gz
tar xzvf libmodplug-0.8.8.5.tar.gz
cd libmodplug-0.8.8.5
./configure
make -j8
make install

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
make -j8
make install

cd ~/ffmpeg_sources
curl -L -O https://lib.openmpt.org/files/libopenmpt/src/libopenmpt-0.2.7025-beta20.1.tar.gz
tar xzvf libopenmpt-0.2.7025-beta20.1.tar.gz
cd libopenmpt-0.2.7025
make -j8
make install

cd ~/ffmpeg_sources
git clone https://github.com/Distrotech/libilbc-webrtc.git
cd libilbc-webrtc
./configure
make -j8
make install

cd ~/ffmpeg_sources
git clone --depth 1 git://source.ffmpeg.org/ffmpeg
cd ffmpeg
PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
    --prefix="$HOME/ffmpeg_build" \
    --pkg-config-flags="--static" \
    --extra-cflags="-I$HOME/ffmpeg_build/include" \
    --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
    --bindir="$HOME/bin" \
    --enable-gpl \
    --enable-nonfree \
    --disable-d3d11va \
    --disable-dxva2 \
#    --enable-decklink \
    --enable-libass \
    --enable-libcelt \
    --enable-libdc1394 \
    --enable-libfdk-aac \
    --enable-libflite \
    --enable-libfontconfig \
    --enable-libfreetype \
    --enable-libfribidi \
    --enable-libgme \
    --enable-libgsm \
    --enable-libilbc \
    --enable-libmodplug \
    --enable-libmp3lame \
    --enable-libopencore-amrnb \
    --enable-libopencore-amrwb \
    --enable-libopenmpt \
    --enable-libopus \
    --enable-libpulse \
    --enable-librtmp \
    --enable-libschroedinger \
    --enable-libsmbclient \
    --enable-libsnappy \
    --enable-libsoxr \
    --enable-libspeex \
    --enable-libssh \
    --enable-libtheora \
    --enable-libtwolame \
    --enable-libv4l2 \
    --enable-libvidstab \
    --enable-libvorbis \
    --enable-libvpx \
    --enable-libwavpack \
    --enable-libx264 \
    --enable-libx265 \
    --enable-libxavs \
    --enable-libxvid \
    --enable-netcdf \
    --enable-openssl \
    --enable-version3
make -j8
make install
make distclean
hash -r
