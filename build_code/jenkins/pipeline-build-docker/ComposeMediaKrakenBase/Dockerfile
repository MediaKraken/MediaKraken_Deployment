# Download base image Ubuntu 16.04
FROM ubuntu:16.04

MAINTAINER Quinn D Granfor, spootdev@gmail.com

# Copy the files so the pip requirements file is there
ADD requirements.txt /home/mediakraken
ADD pipeline-build-os-ffmpeg-ubuntu-1604.sh /home/mediakraken
WORKDIR /home/mediakraken

# Update Software repository
RUN apt-get -y update && apt-get -y install autoconf automake build-essential cifs-utils nfs-common yasm cmake libsnmp-dev libldap2-dev libass-dev libfreetype6-dev python-pip libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev pkg-config texinfo zlib1g-dev libsmbclient-dev libffi-dev libsasl2-dev portaudio19-dev libjpeg-dev autotools-dev autoconf automake build-essential cmake libass-dev libfreetype6-dev libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev pkg-config texinfo zlib1g-dev cmake libsmbclient-dev libffi-dev libldap2-dev libsasl2-dev git curl wget libtool libfreetype6-dev libfribidi-dev libfontconfig1-dev libssh-dev libtwolame-dev libwavpack-dev flite1-dev librtmp-dev libgme-dev libdc1394-22-dev libsoxr-dev libpulse-dev libnetcdf-dev libgsm1-dev libsnappy-dev libschroedinger-dev libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev && mkdir mediakraken/bin && mkdir mediakraken/cache && mkdir mediakraken/conf mkdir mediakraken/key && mkdir mediakraken/log && pip install --upgrade pip && pip install -r requirements.txt && ./pipeline-build-os-ffmpeg-ubuntu-1604.sh && apt-get autoremove && apt-get clean && apt-get autoclean && rm -Rf ~/ffmpeg_sources && rm -Rf ~/ffmpeg_build && rm -Rf ~/bin
