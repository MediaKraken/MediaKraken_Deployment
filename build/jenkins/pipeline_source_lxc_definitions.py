'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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
import pipeline_source_packages_ubuntu

# find all templates in ZFSDir storage
# pvesm list ZFSDir -content vztmpl

SERVERS_TO_BUILD = [
    # 0 - hostname
    # 1 - create vm
    # 2 - lxc image to use
    # 3 - base os name
    # 4 - packages list to install
    # 5 - pip list file to use
    # 6 - IP addr of target
    # VM name, Build lxc, image, package list
    ('SourceAlpine34Server', False, 'imagetouse', 'alpine', [], None, None),
    ('SourceUbuntu1604Server', True, 'ZFSDir:vztmpl/ubuntu-16.04-standard_16.04-1_amd64.tar.gz',\
         'ubuntu', pipeline_source_packages_ubuntu.PACKAGES_SERVER_UBUNTU_1604,\
         'pipeline-build-os-pip-server-ubuntu-1604.txt', '10.0.0.103', None)
]
