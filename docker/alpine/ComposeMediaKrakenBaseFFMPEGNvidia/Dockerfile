# Download base image
FROM mediakraken/mkbasenvidia

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL Description="This image holds the base ffmpeg for slave with nvidia"

RUN mkdir /mediakraken && mkdir /mediakraken/bin
# copy ffmpeg build
ADD pipeline-build-os-ffmpeg-ubuntu.sh /mediakraken
WORKDIR /mediakraken

RUN apt-get update \
  && apt-get -y install \
  autoconf \
  automake \
  build-essential \
  libass-dev \
  libfreetype6-dev \
  libsdl2-dev \
  libtheora-dev \
  libtool \
  libva-dev \
  libvdpau-dev \
  libvorbis-dev \
  libxcb1-dev \
  libxcb-shm0-dev \
  libxcb-xfixes0-dev \
  pkg-config \
  texinfo \
  zlib1g-dev \
  libmp3lame-dev \
  libopus-dev \
  libvorbis-dev \
  libvpx-dev \
  git \
  curl \
  yasm \
  cmake \
  checkinstall \
  libjack-jackd2-dev \
  libopencore-amrnb-dev \
  libopencore-amrwb-dev \
  libsdl1.2-dev \
  libavfilter-dev \
  libx11-dev \
  libxfixes-dev \
  texi2html \
  flite1-dev \
  libgsm1-dev \
  libmodplug-dev \
  librtmp-dev \
  libsmbclient-dev \
  libsnappy-dev \
  libsoxr-dev \
  libspeex-dev \
  libwavpack-dev \
  libxvidcore-dev \
  wget
RUN /mediakraken/pipeline-build-os-ffmpeg-ubuntu.sh \
  && mv ~/bin/ff* /mediakraken/bin/. \
  && rm /mediakraken/bin/ffserver \
  && rm /mediakraken/pipeline-build-os-ffmpeg-ubuntu.sh \
  && rm -Rf ~/ffmpeg_sources && rm -Rf ~/ffmpeg_build && rm -Rf ~/bin
