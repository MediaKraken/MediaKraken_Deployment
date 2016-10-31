# Download base image
FROM alpine:3.4

MAINTAINER Quinn D Granfor, spootdev@gmail.com

LABEL www.mediakraken.org.version="dev-0.1.12"
LABEL www.mediakraken.org.release-date="2016-10-28"
LABEL Description="This image holds the base ffmpeg for server/slave"

RUN apk add --upgrade \
  gcc \
  autoconf \
  automake \
  autotools-dev \
  build-essential \
  cmake \
  curl \
  libdc1394-22-dev \
  flite1-dev \
  git \
  libass-dev \
  libffi-dev \
  libfontconfig1-dev \
  libfreetype6-dev \
  libfribidi-dev \
  libgme-dev \
  libgsm1-dev \
  libldap2-dev \
  libnetcdf-dev \
  libopencore-amrnb-dev \
  libopencore-amrwb-dev \
  libpulse-dev \
  librtmp-dev \
  libsasl2-dev \
  libschroedinger-dev \
  libsdl1.2-dev \
  libsmbclient-dev \
  libsnappy-dev \
  libssh-dev \
  libsoxr-dev \
  libtheora-dev \
  libtool \
  libtwolame-dev \
  libv4l-dev \
  libva-dev \
  libvdpau-dev \
  libvorbis-dev \
  libwavpack-dev \
  libxcb-shm0-dev \
  libxcb-xfixes0-dev \
  libxcb1-dev \
  pkg-config \
  texinfo \
  wget \
  zlib1g-dev \
  && rm -Rf ~/ffmpeg_sources && rm -Rf ~/ffmpeg_build && rm -Rf ~/bin
