# Download base image
FROM mediakraken/mknvidia

LABEL AUTHOR="Quinn D Granfor, spootdev@gmail.com"
LABEL www.mediakraken.org.version="dev-0.2.0"
LABEL Description="This image holds the base ffmpeg for slave with nvidia"

RUN mkdir /mediakraken && mkdir /mediakraken/bin
# copy ffmpeg build
ADD pipeline-build-os-ffmpeg-ubuntu.sh /mediakraken
WORKDIR /mediakraken

RUN apt-get update \
  && sudo apt-get -y install \
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
  && /mediakraken/pipeline-build-os-ffmpeg-ubuntu.sh \
  && mv ~/bin/ff* /bin/. \
  && rm /bin/ffserver \
  && rm /mediakraken/pipeline-build-os-ffmpeg-ubuntu.sh \
  && rm -Rf ~/ffmpeg_sources && rm -Rf ~/ffmpeg_build && rm -Rf ~/bin
