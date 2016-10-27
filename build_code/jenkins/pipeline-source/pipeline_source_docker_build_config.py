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
from shutil import copyfile, rmtree
import os
import sys
sys.path.append('.')
import pipeline_source_packages_ubuntu

DEV_TO_BUILD = 'dev-0.1.12'


def build_base_dir(server_copy=False):
    if server_copy:
        command_string = '&& mkdir /home/mediakraken/backups'\
            ' && mkdir /home/mediakraken/passwordmeter'\
            ' && mkdir /home/mediakraken/passwordmeter/res'
    else:
        command_string = ' && mkdir /home/mediakraken/bin'\
            ' && mkdir /home/mediakraken/cache'\
            ' && mkdir /home/mediakraken/conf'\
            ' && mkdir /home/mediakraken/key'\
            ' && mkdir /home/mediakraken/log'
    return command_string


#nuke old directories
try:
    rmtree('/home/spoot/github/MediaKraken/MediaKraken_Deployment/build_code/'\
           'jenkins/pipeline-build-docker/ComposeMediaKrakenServer/src')
except:
    pass
try:
    rmtree('/home/spoot/github/MediaKraken/MediaKraken_Deployment/build_code/'\
           'jenkins/pipeline-build-docker/ComposeMediaKrakenSlave/src')
except:
    pass

# build image sources
for folder_name in ('fake_donotremove', 'common', 'conf', 'database'): # server, slave
    print('F1: %s' % folder_name)
    os.system('cp -R /home/spoot/github/MediaKraken/MediaKraken_Deployment/' + folder_name\
             + ' /home/spoot/github/MediaKraken/MediaKraken_Deployment/build_code/'\
             'jenkins/pipeline-build-docker/ComposeMediaKrakenServer/src/')
    os.system('cp -R /home/spoot/github/MediaKraken/MediaKraken_Deployment/' + folder_name\
             + ' /home/spoot/github/MediaKraken/MediaKraken_Deployment/build_code/'\
             'jenkins/pipeline-build-docker/ComposeMediaKrakenSlave/src/')
for file_name in ('README.md', 'LICENSE'): # server, slave
    os.system('cp /home/spoot/github/MediaKraken/MediaKraken_Deployment/' + file_name\
             + ' /home/spoot/github/MediaKraken/MediaKraken_Deployment/build_code/'\
             'jenkins/pipeline-build-docker/ComposeMediaKrakenServer/src/.')
    os.system('cp /home/spoot/github/MediaKraken/MediaKraken_Deployment/' + file_name\
             + ' /home/spoot/github/MediaKraken/MediaKraken_Deployment/build_code/'\
             'jenkins/pipeline-build-docker/ComposeMediaKrakenSlave/src/.')

# server
for folder_name in ('metadata', 'network', 'web_app'):
    print('F2: %s' % folder_name)
    os.system('cp -R /home/spoot/github/MediaKraken/MediaKraken_Deployment/' + folder_name\
             + ' /home/spoot/github/MediaKraken/MediaKraken_Deployment/build_code/'\
             'jenkins/pipeline-build-docker/ComposeMediaKrakenServer/src/')
for program_name in ('bulk_gamesdb_netfetch.py',\
        'main_server.py',\
        'main_server_api.py',\
        'main_server_link.py',\
        'main_server_metadata_api.py',\
        'main_server_trigger.py',\
        'subprogram*.py'):
    print('F3: %s' % program_name)
    os.system('cp /home/spoot/github/MediaKraken/MediaKraken_Deployment/' + program_name\
             + ' /home/spoot/github/MediaKraken/MediaKraken_Deployment/build_code/'\
             'jenkins/pipeline-build-docker/ComposeMediaKrakenServer/src/.')

# slave
for program_name in ('main_server_slave.py', ''):
    print('F4: %s' % program_name)
    os.system('cp /home/spoot/github/MediaKraken/MediaKraken_Deployment/' + program_name\
             + ' /home/spoot/github/MediaKraken/MediaKraken_Deployment/build_code/'\
             'jenkins/pipeline-build-docker/ComposeMediaKrakenSlave/src/.')

# build base image
command_string = \
    '# Download base image Ubuntu 16.04\n'\
    'FROM ubuntu:16.04\n'\
    '\n'\
    'MAINTAINER Quinn D Granfor, spootdev@gmail.com\n'\
    '\n'\
    '# Copy the files so the pip requirements file is there\n'\
    'RUN mkdir /home/mediakraken\n'\
    'ADD requirements.txt /home/mediakraken\n'\
    'ADD pipeline-build-os-ffmpeg-ubuntu-1604.sh /home/mediakraken\n'\
    'WORKDIR /home/mediakraken\n'\
    '\n'\
    '# Update Software repository\n'\
    'RUN apt-get -y update && apt-get -y install'
for package_name in pipeline_source_packages_ubuntu.PACKAGES_BASE_UBUNTU_1604:
    command_string += ' ' + package_name
for package_name in pipeline_source_packages_ubuntu.PACKAGES_FFMPEG_UBUNTU_1604:
    command_string += ' ' + package_name
command_string += build_base_dir(False) # create base dirs
command_string += ' && pip install --upgrade pip'\
    ' && pip install -r requirements.txt'\
    ' && ./pipeline-build-os-ffmpeg-ubuntu-1604.sh'\
    ' && apt-get autoremove && apt-get clean && apt-get autoclean'\
    ' && rm -Rf ~/ffmpeg_sources && rm -Rf ~/ffmpeg_build && rm -Rf ~/bin\n'
copyfile('pipeline-build-os-pip-base-ubuntu-1604.txt',\
         '../pipeline-build-docker/ComposeMediaKrakenBase/requirements.txt')
copyfile('pipeline-build-os-ffmpeg-ubuntu-1604.sh',\
         '../pipeline-build-docker/ComposeMediaKrakenBase/'\
         'pipeline-build-os-ffmpeg-ubuntu-1604.sh')
os.system('chmod +x ../pipeline-build-docker/ComposeMediaKrakenBase/'\
         'pipeline-build-os-ffmpeg-ubuntu-1604.sh')
file_handle = open('../pipeline-build-docker/ComposeMediaKrakenBase/Dockerfile', 'w+')
file_handle.write(command_string)
file_handle.close()


# build the slave server
if len(pipeline_source_packages_ubuntu.PACKAGES_SLAVE_UBUNTU_1604) > 0:
    command_string = \
        '# Download base imag\n'\
        'FROM mediakraken/mkbase:' + DEV_TO_BUILD + '\n'\
        '\n'\
        'MAINTAINER Quinn D Granfor, spootdev@gmail.com\n'\
        '\n'\
        '# Copy the files so the pip requirements file is there\n'\
        'ADD src /home/mediakraken\n'\
        'ADD requirements.txt /home/mediakraken\n'\
        'WORKDIR /home/mediakraken\n'\
        '\n'\
        '# Update Software repository\n'\
        'RUN apt-get -y install'
    for package_name in pipeline_source_packages_ubuntu.PACKAGES_SLAVE_UBUNTU_1604:
        command_string += ' ' + package_name
    command_string += ' && '
else:
    command_string = \
        '# Download base image\n'\
        'FROM mediakraken/mkbase:' + DEV_TO_BUILD + '\n'\
        '\n'\
        'MAINTAINER Quinn D Granfor, spootdev@gmail.com\n'\
        '\n'\
        '# Copy the files so the pip requirements file is there\n'\
        'ADD src /home/mediakraken\n'\
        'ADD requirements.txt /home/mediakraken\n'\
        'WORKDIR /home/mediakraken\n'\
        '\n'\
        '# Update Software repository\n'\
        'RUN '
command_string += 'pip install -r requirements.txt'\
    ' && apt-get autoremove && apt-get clean && apt-get autoclean'
command_string += '\nENTRYPOINT ["python", "/home/mediakraken/main_server_slave.py"]\n'
copyfile('pipeline-build-os-pip-slave-ubuntu-1604.txt',\
         '../pipeline-build-docker/ComposeMediaKrakenSlave/requirements.txt')
file_handle = open('../pipeline-build-docker/ComposeMediaKrakenSlave/Dockerfile', 'w+')
file_handle.write(command_string)
file_handle.close()


# build the server
if len(pipeline_source_packages_ubuntu.PACKAGES_SERVER_UBUNTU_1604) > 0:
    command_string = \
        '# Download base image\n'\
        'FROM mediakraken/mkbase:' + DEV_TO_BUILD + '\n'\
        '\n'\
        'MAINTAINER Quinn D Granfor, spootdev@gmail.com\n'\
        '\n'\
        '# Copy the files so the pip requirements file is there\n'\
        'ADD src /home/mediakraken\n'\
        'ADD requirements.txt /home/mediakraken\n'\
        'WORKDIR /home/mediakraken\n'\
        '\n'\
        '# Update Software repository\n'\
        'RUN apt-get -y install'
    for package_name in pipeline_source_packages_ubuntu.PACKAGES_SERVER_UBUNTU_1604:
        command_string += ' ' + package_name
    command_string += ' && '
else:
    command_string = \
        '# Download base image\n'\
        'FROM mediakraken/mkbase:' + DEV_TO_BUILD + '\n'\
        '\n'\
        'MAINTAINER Quinn D Granfor, spootdev@gmail.com\n'\
        '\n'\
        '# Copy the files so the pip requirements file is there\n'\
        'ADD src /home/mediakraken\n'\
        'ADD requirements.txt /home/mediakraken\n'\
        'WORKDIR /home/mediakraken\n'\
        '\n'\
        '# Update Software repository\n'\
        'RUN '
command_string += 'pip install -r requirements.txt'\
    ' && apt-get autoremove && apt-get clean && apt-get autoclean'
command_string += build_base_dir(True) # create server dirs
command_string += '\nENTRYPOINT ["python", "/home/mediakraken/main_server.py"]\n'
copyfile('pipeline-build-os-pip-server-ubuntu-1604.txt',\
         '../pipeline-build-docker/ComposeMediaKrakenServer/requirements.txt')
file_handle = open('../pipeline-build-docker/ComposeMediaKrakenServer/Dockerfile', 'w+')
file_handle.write(command_string)
file_handle.close()
