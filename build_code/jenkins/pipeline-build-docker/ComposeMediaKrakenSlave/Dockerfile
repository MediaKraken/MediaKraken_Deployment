# Download base image Ubuntu 16.04
FROM ubuntu:16.04

MAINTAINER spootdev@gmail.com

# Update Software repository
RUN apt-get -y update && apt-get -y install autoconf automake build-essential libass-dev libfreetype6-dev libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev pkg-config texinfo zlib1g-dev yasm cmake libsmbclient-dev libffi-dev libsnmp-dev libldap2-dev libsasl2-dev portaudio19-dev nfs-common cifs-utils python-pip && pip install --upgrade pip && pip install -r requirements.txt