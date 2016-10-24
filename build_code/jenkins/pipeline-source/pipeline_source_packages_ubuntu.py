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
import logging # pylint: disable=W0611


PACKAGES_BASE_UBUNTU_1604 = [
    'autoconf',
    'automake',
    'build-essential',
    'cifs-utils',
    'nfs-common',
    'yasm',
    'cmake',
    'libsnmp-dev',
    'libldap2-dev',
    'libass-dev',
    'libfreetype6-dev',
    'python-pip',
    'libsdl1.2-dev',
    'libtheora-dev',
    'libtool',
    'libva-dev',
    'libvdpau-dev',
    'libvorbis-dev',
    'libxcb1-dev',
    'libxcb-shm0-dev',
    'libxcb-xfixes0-dev',
    'pkg-config',
    'texinfo',
    'zlib1g-dev',
    'libsmbclient-dev',
    'libffi-dev',
    'libsasl2-dev',
    'portaudio19-dev',
    'libjpeg-dev',
    ]


PACKAGES_SERVER_UBUNTU_1604 = [
    'libdiscid-dev',
    'postgresql-server-dev-9.5',
    'nginx',
    'redis-server',
    ]


PACKAGES_SLAVE_UBUNTU_1604 = [
    ]


PACKAGES_FFMPEG_UBUNTU_1604 = [
    'autotools-dev',
    'autoconf',
    'automake',
    'build-essential',
    'cmake',
    'libass-dev',
    'libfreetype6-dev',
    'libsdl1.2-dev',
    'libtheora-dev',
    'libtool',
    'libva-dev',
    'libvdpau-dev',
    'libvorbis-dev',
    'libxcb1-dev',
    'libxcb-shm0-dev',
    'libxcb-xfixes0-dev',
    'pkg-config',
    'texinfo',
    'zlib1g-dev',
    'cmake',
    'libsmbclient-dev',
    'libffi-dev',
    'libldap2-dev',
    'libsasl2-dev',
    'git',
    'curl',
    'wget',
    'libtool',
    'libfreetype6-dev',
    'libfribidi-dev',
    'libfontconfig1-dev',
    'libssh-dev',
    'libtwolame-dev',
    'libwavpack-dev',
    'flite1-dev',
    'librtmp-dev',
    'libgme-dev',
    'libdc1394-22-dev',
    'libsoxr-dev',
    'libpulse-dev',
    'libnetcdf-dev',
    'libgsm1-dev',
    'libsnappy-dev',
    'libschroedinger-dev',
    'libopencore-amrnb-dev',
    'libopencore-amrwb-dev',
    'libv4l-dev',
    ]
