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
from shutil import copyfile
import sys
sys.path.append('.')
import pipeline_source_packages_ubuntu


header_file_lines =\
    '# Download base image Ubuntu 16.04\n'\
    'FROM ubuntu:16.04\n'\
    '\n'\
    'MAINTAINER spootdev@gmail.com\n'\
    '\n'\
    '# Update Software repository\n'\
    'RUN apt-get -y update && apt_get -y install'\

# build the slave server
command_string = header_file_lines
for package_name in pipeline_source_packages_ubuntu.PACKAGES_SLAVE_UBUNTU_1604:
    command_string += ' ' + package_name
command_string += ' && pip install -r requirements.txt'
copyfile('pipeline-build-os-pip-slave-ubuntu-1604.txt',\
         '../pipeline-build-docker/ComposeMediaKrakenSlave/requirements.txt')
file_handle = open('../pipeline-build-docker/ComposeMediaKrakenSlave/Dockerfile', 'w+')
file_handle.write(command_string)
file_handle.close()
