FROM ubuntu:18.10 as builder

ARG PIPMIRROR

ENV PKG_CONFIG_PATH=/usr/local/lib/pkgconfig \
    SRC=/usr/local

ARG FDKAAC_VERSION=0.1.5
ARG X264_VERSION=20181217-2245-stable
ARG X265_VERSION=2.9
ARG FFMPEG_VERSION="4.1"
ARG OPENMPT_VERSION=0.2.8760-beta27

COPY scripts /mediakraken
RUN mkdir /mediakraken/install
COPY scripts/vid.stab.0.98b /mediakraken/install/vid.stab.0.98b
RUN mkdir /mediakraken/cuda
ADD cuda /mediakraken/cuda

# will need to add/comipile by hand as dev version doesn't exist
# rtmpdump-dev \

RUN buildDeps="autoconf \
        automake \
        build-essential \
        cmake \
        curl \
        libfontconfig1-dev \
        git \
        gnutls-dev \
        libmp3lame-dev \
        libass-dev \
        libmodplug-dev \
        libogg-dev \
        libtheora-dev \
        libtool \
        libva-dev \
        libvdpau-dev \
        libvorbis-dev \
        libvpx-dev \
        libwebp-dev \
        nasm \
        libopenjp2-7-dev \
        libopus-dev \
        libsmbclient-dev \
        python3-dev \
        samba-dev \
        libspeex-dev \
        libsoxr-dev \
        libxvidcore-dev \
        yasm" && \
    export MAKEFLAGS="-j$(($(grep -c ^processor /proc/cpuinfo) + 1))" && \
    apt update && \
    apt -y upgrade && \
    apt -y install apt-utils ${buildDeps} libgcc1 ca-certificates && \
    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -L --insecure https://ftp.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-${X264_VERSION}.tar.bz2 | \
    tar -jx --strip-components=1 && \
    ./configure --prefix="${SRC}" --bindir="${SRC}/bin" --enable-pic --enable-shared --disable-cli && \
    make -j`getconf _NPROCESSORS_ONLN` && \
    make install && \
    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -L --insecure https://get.videolan.org/x265/x265_${X265_VERSION}.tar.gz | \
    tar -zx --strip-components=1 && \
    cd build/linux && \
    cmake -G "Unix Makefiles" ../../source && \
    make -j`getconf _NPROCESSORS_ONLN` && \
    make install && \
    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -L --insecure https://github.com/mstorsjo/fdk-aac/archive/v${FDKAAC_VERSION}.tar.gz | \
    tar -zx --strip-components=1 && \
    autoreconf -fiv && \
    ./configure --prefix="${SRC}" --disable-static --datadir="${DIR}" && \
    make -j`getconf _NPROCESSORS_ONLN` && \
    make install && \
    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -L --insecure https://lib.openmpt.org/files/libopenmpt/src/libopenmpt-${OPENMPT_VERSION}.tar.gz | \
    tar -zx --strip-components=1 && \
    make EXAMPLES=0 && \
    make install && \
    chmod +x /mediakraken/*.sh && \
    /mediakraken/kvazaar.sh && \
    /mediakraken/openh264.sh && \
    /mediakraken/vidstab.sh && \
    # nvenc headers for ffmpeg
    git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git && \
    cd nv-codec-headers && \
    make -j`getconf _NPROCESSORS_ONLN` && \
    make install && \
    # Make the run file executable and extract
    chmod +x /mediakraken/cuda/cuda_*_linux.run && \
    cd /mediakraken/cuda && \
    ./cuda_*_linux.run --tar mxvf && \
    ./cuda-installer.pl --silent --toolkit --no-opengl-libs --no-man-page && \
    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -LO --insecure http://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz && \
    tar -zx --strip-components=1 -f ffmpeg-${FFMPEG_VERSION}.tar.gz && \
#         --enable-librtmp 
   ./configure \
	--target-os=linux \
        --bindir="${SRC}/bin" \
        --extra-libs=-ldl \
        --extra-cflags="-I${SRC}/include" \
        --extra-ldflags="-L${SRC}/lib" \
        --extra-cflags="-I/usr/local/cuda-10.0/include/" \
        --extra-ldflags=-L/usr/local/cuda-10.0/lib64/ \
        --prefix="${SRC}" \
        --enable-avfilter \
        --enable-avresample \
        --enable-fontconfig \
        --enable-cuda \
        --enable-cuvid \
        --enable-gpl \
        --enable-libass \
        --enable-libfdk_aac \
        --enable-fontconfig \
        --enable-libfreetype \
        --enable-libkvazaar \
        --enable-libmodplug \
        --enable-libmp3lame \
        --enable-libopenh264 \
        --enable-libopenjpeg \
        --enable-libopenmpt \
        --enable-libopus \
        --enable-libsoxr \
        --enable-libsmbclient \
        --enable-libspeex \
        --enable-libtheora \
        --enable-libwebp \
        --enable-vaapi \
        --enable-libvidstab \
        --enable-libvorbis \
        --enable-libvpx \
        --enable-libx264 \
        --enable-libx265 \
        --enable-libxvid \
        --enable-nonfree \
        --enable-nvenc \
        --enable-postproc \
        --enable-pthreads \
        --enable-shared \
        --enable-small \
        --enable-vdpau \
        --enable-version3 \
        --enable-zlib \
        --disable-debug \
        --disable-doc \
        --disable-static \
        --disable-ffplay && \
    make -j`getconf _NPROCESSORS_ONLN` && \
    make install && \
    hash -r
    
FROM ubuntu:18.10

COPY --from=builder /usr/local/bin/ffmpeg /usr/local/bin/ffmpeg
COPY --from=builder /usr/local/bin/ffprobe /usr/local/bin/ffprobe
COPY --from=builder /usr/local/lib /usr/local/lib

ARG NVIDIA_DRIVER=415.25

RUN mkdir /mediakraken
ADD driver /mediakraken

RUN apt update && \
    apt -y upgrade && \
    apt -y install smbclient lame libass9 libmodplug1 libogg0 \
        libtheora0 libvorbis0a libopus0 libspeex1 libxvidcore4 \
        libfreetype6 libopenjp2-7-dev webp libsoxr0 fontconfig \
        libvpx5 libva2 libvdpau1 xz-utils libva-drm2 libvorbisfile3 \
        kmod libopengl0 libegl1 && \
    chmod +x /mediakraken/NVIDIA-Linux-x86_64-*.run && \
    cd /mediakraken && \
    ./NVIDIA-Linux-x86_64-${NVIDIA_DRIVER}.run -s -N --no-kernel-module && \
    rm -Rf /mediakraken && \
    rm -rf /var/lib/apt/lists/* && \
    ffmpeg -buildconf

CMD ["--help"]
WORKDIR /tmp/ffmpeg

