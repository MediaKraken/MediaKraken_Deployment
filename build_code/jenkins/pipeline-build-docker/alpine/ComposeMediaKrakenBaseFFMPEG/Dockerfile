# Download base image
FROM alpine:3.4

MAINTAINER Quinn D Granfor, spootdev@gmail.com

LABEL www.mediakraken.org.version="dev-0.1.12"
LABEL www.mediakraken.org.release-date="2016-10-28"
LABEL Description="This image holds the base ffmpeg for server/slave"

RUN mkdir /mediakraken
# copy ffmpeg build
ADD pipeline-build-os-ffmpeg-alpine.sh /mediakraken
WORKDIR /mediakraken

RUN apk add --update \
  python \
  alpine-sdk \
  yasm-dev \
  autoconf \
  automake \
  cmake \
  flite-dev \
  libass-dev \
  libffi-dev \
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
  && /mediakraken/pipeline-build-os-ffmpeg-alpine.sh \
  && rm -Rf ~/ffmpeg_sources && rm -Rf ~/ffmpeg_build && rm -Rf ~/bin \
  && apk del \
  alpine-sdk \
  yasm-dev
