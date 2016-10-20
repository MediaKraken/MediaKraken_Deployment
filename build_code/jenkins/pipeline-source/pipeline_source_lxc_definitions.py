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
import pipeline_source_packages_ubuntu
import pipeline_source_pip_definitions_ubuntu


# find all templates in ZFSDir storage
# pvesm list ZFSDir -content vztmpl


BUILD_BRANCH = 'dev-0.1.11'
SERVERS_TO_BUILD = [
    # VM name, Build lxc, image, package list
    ('SourceAlpine33', False, 'imagetouse', 'alpine', [], []),
    ('SourceAlpine34', False, 'imagetouse', 'alpine', [], []),
    ('SourceDebian84', False, 'imagetouse', 'debian', [], []),
    ('SourceDebian85', False, 'imagetouse', 'debian', [], []),
    ('SourceDebian86', False, 'imagetouse', 'debian', [], []),
    ('SourceUbuntu1504', False, 'imagetouse', 'ubuntu', [], []),
    ('SourceUbuntu1510', False, 'imagetouse', 'ubuntu', [], []),
    ('SourceUbuntu1604', True, 'ZFSDir:vztmpl/ubuntu-16.04-standard_16.04-1_amd64.tar.gz',\
         'ubuntu', pipeline_source_packages_ubuntu.PACKAGES_UBUNTU_1604,\
         pipeline_source_pip_definitions_ubuntu.PIP_UBUNTU_1604),
    ]
