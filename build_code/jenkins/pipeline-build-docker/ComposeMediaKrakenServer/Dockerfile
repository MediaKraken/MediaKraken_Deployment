# Download base image Ubuntu 16.04
FROM ubuntu:16.04

MAINTAINER spootdev@gmail.com

# Copy the files so the pip requirements file is there
ADD . /code
WORKDIR /code

# Update Software repository
RUN apt-get -y update && apt-get -y install autoconf automake build-essential libass-dev libfreetype6-dev libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev pkg-config texinfo zlib1g-dev yasm cmake libsmbclient-dev python-pip postgresql-server-dev-9.5 libffi-dev libsnmp-dev libldap2-dev libsasl2-dev libjpeg-dev libdiscid-dev portaudio19-dev nfs-common nginx redis-server cifs-utils && pip install --upgrade pip && pip install -r requirements.txt