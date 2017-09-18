FROM alpine:3.6 as builder

ENV PKG_CONFIG_PATH=/usr/local/lib/pkgconfig \
    SRC=/usr/local

ARG FDKAAC_VERSION=0.1.5
ARG LAME_VERSION=3.99.5
ARG X264_VERSION=20170917-2245-stable
ARG X265_VERSION=2.5
ARG FFMPEG_VERSION="3.3.4"
ARG SPEEX_VERSION=1.2.0
ARG OPENMPT_VERSION=0.2.8760-beta27
ARG XVID_VERSION=1.3.4

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
        gnupg \
        gnutls-dev \
        libogg-dev \
        libstdc++ \
        libtheora-dev \
        libtool \
        libvorbis-dev \
        make \
        opus-dev \
        python \
        python-dev \
        openssl-dev \
        samba-dev \
        tar \
	yasm \
        zlib-dev" && \
    export MAKEFLAGS="-j$(($(grep -c ^processor /proc/cpuinfo) + 1))" && \
    apk update && \
    apk upgrade && \
    apk add --update ${buildDeps} libgcc libstdc++ ca-certificates libssl1.0 && \
    
    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -sL https://ftp.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-${X264_VERSION}.tar.bz2 | \
    tar -jx --strip-components=1 && \
    ./configure --prefix="${SRC}" --bindir="${SRC}/bin" --enable-pic --enable-shared --disable-cli && \
    make && \
    make install && \

    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -sL https://get.videolan.org/x265/x265_${X265_VERSION}.tar.gz | \
    tar -zx --strip-components=1 && \
    cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="${SRC}" -DENABLE_SHARED:bool=off ./source && \
    make && \
    make install && \

    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -sL https://downloads.sf.net/project/lame/lame/${LAME_VERSION%.*}/lame-${LAME_VERSION}.tar.gz | \
    tar -zx --strip-components=1 && \
    ./configure --prefix="${SRC}" --bindir="${SRC}/bin" --disable-static --enable-nasm --datarootdir="${DIR}" && \
    make && \
    make install && \

    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -sL https://github.com/mstorsjo/fdk-aac/archive/v${FDKAAC_VERSION}.tar.gz | \
    tar -zx --strip-components=1 && \
    autoreconf -fiv && \
    ./configure --prefix="${SRC}" --disable-static --datadir="${DIR}" && \
    make && \
    make install && \

    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -sL http://downloads.xiph.org/releases/speex/speex-${SPEEX_VERSION}.tar.gz | \
    tar -zx --strip-components=1 && \
    ./configure && \
    make && \
    make install && \

    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -sL https://github.com/MediaKraken/MediaKraken_Submodules/raw/master/libmodplug-0.8.8.5.tar.gz | \
    tar -zx --strip-components=1 && \
    ./configure && \
    make && \
    make install && \

    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -sL https://lib.openmpt.org/files/libopenmpt/src/libopenmpt-${OPENMPT_VERSION}.tar.gz | \
    tar -zx --strip-components=1 && \
    make && \
    make install && \
                
    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -sL http://downloads.xvid.org/downloads/xvidcore-${XVID_VERSION}.tar.gz | \
    tar -zx --strip-components=1 && \
    cd build/generic && \
    ./configure && \
    make && \
    make install && \

    DIR=$(mktemp -d) && cd ${DIR} && \
    curl -sLO http://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz && \
    tar -zx --strip-components=1 -f ffmpeg-${FFMPEG_VERSION}.tar.gz && \
    ./configure \
        --bindir="${SRC}/bin" \
        --extra-libs=-ldl \
        --extra-cflags="-I${SRC}/include" \
        --extra-ldflags="-L${SRC}/lib" \
        --prefix="${SRC}" \
        --enable-nonfree \
        --enable-gpl \
        --enable-version3 \
        --enable-avresample \
        --enable-libmp3lame \
        --enable-libopus \        
        --enable-libx264 \
        --enable-openssl \
        --enable-postproc \
        --enable-small \
        --enable-libfdk_aac \
        --enable-libspeex \
        --enable-libvorbis \
        --enable-libxvid \
        --enable-libsmbclient \
        --enable-libtheora \
        --enable-shared \
        --disable-debug \
        --disable-doc \
        --disable-static \
        --disable-ffserver && \
    make && \
    make install && \
    hash -r
    
FROM alpine:3.6

COPY --from=builder /usr/local/bin/ffmpeg /usr/local/bin/ffmpeg
COPY --from=builder /usr/local/bin/ffprobe /usr/local/bin/ffprobe
COPY --from=builder /usr/local/lib /usr/local/lib

RUN apk add --update libssl1.0 && \
    ffmpeg -buildconf

CMD ["--help"]
ENTRYPOINT  ["ffmpeg"]
WORKDIR /tmp/ffmpeg
