# Download base image Ubuntu 16.04
FROM ubuntu:16.04

MAINTAINER Quinn D Granfor, spootdev@gmail.com

# Copy the files so the pip requirements file is there
RUN mkdir /home/mediakraken
ADD requirements.txt /home/mediakraken
ADD pipeline-build-os-ffmpeg-ubuntu-1604.sh /home/mediakraken
WORKDIR /home/mediakraken

# Update Software repository
RUN apt-get -y update && apt-get -y install autoconf automake build-essential cifs-utils cmake libass-dev libffi-dev libfreetype6-dev libjpeg-dev libldap2-dev libsasl2-dev libsdl1.2-dev libsmbclient-dev libsnmp-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb-shm0-dev libxcb-xfixes0-dev libxcb1-dev nfs-common pkg-config portaudio19-dev python-pip texinfo yasm zlib1g-dev autoconf automake autotools-dev build-essential cmake curl libdc1394-22-dev flite1-dev git libass-dev libffi-dev libfontconfig1-dev libfreetype6-dev libfribidi-dev libgme-dev libgsm1-dev libldap2-dev libnetcdf-dev libopencore-amrnb-dev libopencore-amrwb-dev libpulse-dev librtmp-dev libsasl2-dev libschroedinger-dev libsdl1.2-dev libsmbclient-dev libsnappy-dev libssh-dev libsoxr-dev libtheora-dev libtool libtwolame-dev libv4l-dev libva-dev libvdpau-dev libvorbis-dev libwavpack-dev libxcb-shm0-dev libxcb-xfixes0-dev libxcb1-dev pkg-config texinfo wget zlib1g-dev && mkdir /home/mediakraken/bin && mkdir /home/mediakraken/cache && mkdir /home/mediakraken/conf && mkdir /home/mediakraken/key && mkdir /home/mediakraken/log && pip install --upgrade pip && pip install -r requirements.txt && ./pipeline-build-os-ffmpeg-ubuntu-1604.sh && apt-get autoremove && apt-get clean && apt-get autoclean && rm -Rf ~/ffmpeg_sources && rm -Rf ~/ffmpeg_build && rm -Rf ~/bin
