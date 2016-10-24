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
from shutil import copyfile
import os
import sys
sys.path.append('.')
import pipeline_source_packages_ubuntu


header_file_lines =\
    '# Download base image Ubuntu 16.04\n'\
    'FROM ubuntu:16.04\n'\
    '\n'\
    'MAINTAINER Quinn D Granfor, spootdev@gmail.com\n'\
    '\n'\
    '# Copy the files so the pip requirements file is there\n'\
    'ADD . /mediakraken\n'\
    'WORKDIR /mediakraken\n'\
    '\n'\
    '# Update Software repository\n'\
    'RUN apt-get -y update && apt-get -y install'\

# build the slave server
command_string = header_file_lines
for package_name in pipeline_source_packages_ubuntu.PACKAGES_SLAVE_UBUNTU_1604:
    command_string += ' ' + package_name
for package_name in pipeline_source_packages_ubuntu.PACKAGES_FFMPEG_UBUNTU_1604:
    command_string += ' ' + package_name
command_string += ' && pip install --upgrade pip && pip install -r requirements.txt'\
    ' && ./pipeline-build-os-ffmpeg-ubuntu-1604.sh'\
    ' && apt-get autoremove && apt-get clean && apt-get autoclean'\
    ' && rm -Rf ~/ffmpeg_sources && rm -Rf ~/ffmpeg_build && rm -Rf ~/bin\n'
command_string += 'ENTRYPOINT ["python", "main_server_slave.py"]\n'
copyfile('pipeline-build-os-pip-slave-ubuntu-1604.txt',\
         '../pipeline-build-docker/ComposeMediaKrakenSlave/requirements.txt')
copyfile('pipeline-build-os-ffmpeg-ubuntu-1604.sh',\
         '../pipeline-build-docker/ComposeMediaKrakenSlave/'\
         'pipeline-build-os-ffmpeg-ubuntu-1604.sh')
os.system('chmod +x ../pipeline-build-docker/ComposeMediaKrakenSlave/'\
         'pipeline-build-os-ffmpeg-ubuntu-1604.sh')
file_handle = open('../pipeline-build-docker/ComposeMediaKrakenSlave/Dockerfile', 'w+')
file_handle.write(command_string)
file_handle.close()

# build the server
command_string = header_file_lines
for package_name in pipeline_source_packages_ubuntu.PACKAGES_SERVER_UBUNTU_1604:
    command_string += ' ' + package_name
for package_name in pipeline_source_packages_ubuntu.PACKAGES_FFMPEG_UBUNTU_1604:
    command_string += ' ' + package_name
command_string += ' && pip install --upgrade pip && pip install -r requirements.txt'\
    ' && ./pipeline-build-os-ffmpeg-ubuntu-1604.sh'\
    ' && apt-get autoremove && apt-get clean && apt-get autoclean'\
    ' && rm -Rf ~/ffmpeg_sources && rm -Rf ~/ffmpeg_build && rm -Rf ~/bin\n'
command_string += 'ENTRYPOINT ["python", "main_server.py"]\n'
copyfile('pipeline-build-os-pip-server-ubuntu-1604.txt',\
         '../pipeline-build-docker/ComposeMediaKrakenServer/requirements.txt')
copyfile('pipeline-build-os-ffmpeg-ubuntu-1604.sh',\
         '../pipeline-build-docker/ComposeMediaKrakenServer/'\
         'pipeline-build-os-ffmpeg-ubuntu-1604.sh')
os.system('chmod +x ../pipeline-build-docker/ComposeMediaKrakenServer/'\
         'pipeline-build-os-ffmpeg-ubuntu-1604.sh')
file_handle = open('../pipeline-build-docker/ComposeMediaKrakenServer/Dockerfile', 'w+')
file_handle.write(command_string)
file_handle.close()


# TODO - need to wipe out the temp ffmpeg directories
# --no-install-recommends   ?
# remove curl and wget?
