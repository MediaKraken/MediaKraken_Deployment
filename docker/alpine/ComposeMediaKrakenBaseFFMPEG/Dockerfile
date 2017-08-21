# Download base image
FROM alpine:3.6

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the base ffmpeg for slave"

RUN mkdir /mediakraken && mkdir /mediakraken/bin
# copy ffmpeg build
ADD pipeline-build-os-ffmpeg-alpine.sh /mediakraken
WORKDIR /mediakraken

RUN apk add --update \
  nasm \
  libsmbclient \
  gettext \
  lame-dev \
  opus-dev \
  libogg-dev \
  libvorbis-dev \
  speex-dev \
  xvidcore-dev \
  libtheora-dev \
  openrc \
  alpine-sdk \
  yasm \
  yasm-dev \
  autoconf \
  automake \
  cmake \
  flite-dev \
  libass-dev \
  libffi-dev \
  libmodplug-dev \
  libvpx-dev \
  fontconfig-dev \
  freetype-dev \
  fribidi-dev \
  gpgme-dev \
  gsm-dev \
  rtmpdump-dev \
  libgsasl-dev \
  sdl-dev \
  snappy-dev \
  libssh-dev \
  soxr-dev \
  libtool \
  v4l-utils-dev \
  libva-dev \
  libvdpau-dev \
  wavpack-dev \
  texinfo \
  wget \
  zlib-dev \
  python-dev \
  gnutls-dev \
  samba-dev \
  libressl-dev
RUN /mediakraken/pipeline-build-os-ffmpeg-alpine.sh \
  && mv ~/bin/ff* /mediakraken/bin/. \
  && rm /mediakraken/bin/ffserver \
  && rm /mediakraken/pipeline-build-os-ffmpeg-alpine.sh \
  && rm -Rf ~/ffmpeg_sources && rm -Rf ~/ffmpeg_build && rm -Rf ~/bin \
  && apk del \
  alpine-sdk \
  yasm-dev \
  && rm -rf /var/cache/apk/*
