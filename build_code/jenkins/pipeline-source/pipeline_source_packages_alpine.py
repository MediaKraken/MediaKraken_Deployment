'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
'''


from __future__ import absolute_import, division, print_function, unicode_literals


PACKAGES_BASE_ALPINE_34 = [
    'autoconf',
    'automake',
    'build-essential',
    'cifs-utils',
    'cmake',
    'libass-dev',
    'libffi-dev',
    'libfreetype6-dev',
    'libjpeg-dev',
    'libldap2-dev',
    'libsasl2-dev',
    'libsdl1.2-dev',
    'libsmbclient-dev',
    'libsnmp-dev',
    'libtheora-dev',
    'libtool',
    'libva-dev',
    'libvdpau-dev',
    'libvorbis-dev',
    'libxcb-shm0-dev',
    'libxcb-xfixes0-dev',
    'libxcb1-dev',
    'nfs-common',
    'pkg-config',
    'portaudio19-dev',
    'python-pip',
    'texinfo',
    'yasm',
    'zlib1g-dev',
    ]


PACKAGES_SERVER_ALPINE_34 = [
    'nginx',
    'postgresql-server-dev',
    'redis-server',
    ]


PACKAGES_SLAVE_ALPINE_34 = [
    ]


PACKAGES_THEATER_ALPINE_34 = [
    'libdiscid-dev',
    'python-pip',
    ]


PACKAGES_METADATA_ALPINE_34 = [
    ]


PACKAGES_FFMPEG_ALPINE_34 = [
    'autoconf',
    'automake',
    'autotools-dev',
    'build-essential',
    'cmake',
    'curl',
    'libdc1394-22-dev',
    'flite1-dev',
    'git',
    'libass-dev',
    'libffi-dev',
    'libfontconfig1-dev',
    'libfreetype6-dev',
    'libfribidi-dev',
    'libgme-dev',
    'libgsm1-dev',
    'libldap2-dev',
    'libnetcdf-dev',
    'libopencore-amrnb-dev',
    'libopencore-amrwb-dev',
    'libpulse-dev',
    'librtmp-dev',
    'libsasl2-dev',
    'libschroedinger-dev',
    'libsdl1.2-dev',
    'libsmbclient-dev',
    'libsnappy-dev',
    'libssh-dev',
    'libsoxr-dev',
    'libtheora-dev',
    'libtool',
    'libtwolame-dev',
    'libv4l-dev',
    'libva-dev',
    'libvdpau-dev',
    'libvorbis-dev',
    'libwavpack-dev',
    'libxcb-shm0-dev',
    'libxcb-xfixes0-dev',
    'libxcb1-dev',
    'pkg-config',
    'texinfo',
    'wget',
    'zlib1g-dev',
    ]
