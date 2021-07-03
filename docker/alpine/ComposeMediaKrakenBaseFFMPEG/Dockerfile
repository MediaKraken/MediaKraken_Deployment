FROM alpine:3.13.5 as builder

ARG ALPMIRROR
ARG PIPMIRROR

ENV PKG_CONFIG_PATH=/usr/local/lib/pkgconfig \
    SRC=/usr/local

ARG FDKAAC_VERSION=0.1.5
ARG X264_VERSION=20191217-2245-stable
ARG X265_VERSION=3.4
ARG FFMPEG_VERSION="4.4"
ARG OPENMPT_VERSION=0.2.8760-beta27

COPY scripts /mediakraken
RUN mkdir /mediakraken/install
COPY scripts/vid.stab.0.98b /mediakraken/install/vid.stab.0.98b

RUN buildDeps="autoconf \
        automake \
        bash \
        binutils \
        bzip2 \
        cmake \
        curl \
        coreutils \
        g++ \
        gcc \
        git \
        gnupg \
        gnutls-dev \
        fontconfig-dev \
        freetype-dev \
        lame-dev \
        libass-dev \
        libmodplug-dev \
        libogg-dev \
        rtmpdump-dev \
        libtheora-dev \
        libtool \
        libva-dev \
        libvdpau-dev \
        libvorbis-dev \
        libvpx-dev \
        libwebp-dev \
        make \
        nasm \
        openjpeg-dev \
        opus-dev \
        python3-dev \
        samba-dev \
        speex-dev \
        soxr-dev \
        tar \
        xvidcore-dev \
        xz \
        yasm \
        zlib-dev" && \
    export MAKEFLAGS="-j$(($(grep -c ^processor /proc/cpuinfo) + 1))" && \
    apk add --no-cache ${buildDeps} libgcc==10.2.1_pre1-r3 libstdc++==10.2.1_pre1-r3 ca-certificates==20191127-r5 busybox==1.32.1-r6 && \
    DIR=$(mktemp -d) && cd ${DIR} && \
    git clone https://code.videolan.org/videolan/x264.git && \
    cd x264 && \
    ./configure --prefix="${SRC}" --bindir="${SRC}/bin" --enable-pic --enable-shared --disable-cli && \
    make -j`getconf _NPROCESSORS_ONLN` && \
    make install && \
    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -L --insecure https://github.com/videolan/x265/archive/${X265_VERSION}.tar.gz | \
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
    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -LO --insecure http://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz && \
    tar -zx --strip-components=1 -f ffmpeg-${FFMPEG_VERSION}.tar.gz && \
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
        --enable-librtmp \
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
    
FROM alpine:3.13.5

COPY --from=builder /usr/local/bin/ffmpeg /usr/local/bin/ffmpeg
COPY --from=builder /usr/local/bin/ffprobe /usr/local/bin/ffprobe
COPY --from=builder /usr/local/lib /usr/local/lib

# busybox isn't r6 due to other dependancy
RUN apk add --no-cache \
    busybox==1.32.1-r6 \
    bash==5.1.0-r0 \
    samba-client==4.13.8-r0 \
    lame==3.100-r0 \
    libass==0.15.0-r0 \
    libmodplug==0.8.9.0-r0 \
    libogg==1.3.4-r0 \
    libtheora==1.1.1-r16 \
    libvorbis==1.3.7-r0 \
    opus==1.3.1-r1 \
    speex==1.2.0-r0 \
    xvidcore==1.3.7-r1 \
    freetype==2.10.4-r1 \
    zlib==1.2.11-r3 \
    openjpeg==2.4.0-r1 \
    libwebp==1.1.0-r0 \
    soxr==0.1.3-r2 \
    fontconfig==2.13.1-r3 \
    libvpx==1.9.0-r0 \
    librtmp==2.4_git20190330-r1 \
    libva==2.10.0-r0 \
    libvdpau==1.4-r0 \
    libva-intel-driver==2.4.1-r0 \
    && rm -Rf /home/* && \
    ffmpeg -buildconf

# will create gid 1000 error in later images
#   adduser -DHs /sbin/nologin metaman
# Do NOT do the below as other containers won't have rights to install/build.
# USER metaman

CMD ["--help"]
WORKDIR /tmp/ffmpeg
