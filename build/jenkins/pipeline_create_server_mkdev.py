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
import time
import os
from common import common_network_ssh
from common import common_network_vm_proxmox


###
# Will be used to build the deps like FFMPEG
###
JENKINS_BUILD_UBUNTU_VIM_LXC = 103
JENKINS_BUILD_UBUNTU_VIM_LNX_IP = '10.0.0.90'
FFMPEG_BRANCH = 'dev-0.1.11'


# create prox class instance to use
PROX_CONNECTION = common_network_vm_proxmox.CommonNetworkProxMox('10.0.0.190', 'root@pam',\
    'jenkinsbuild')


# check status of ubuntu build vm
if PROX_CONNECTION.com_net_prox_node_lxc_status('pve',\
        JENKINS_BUILD_UBUNTU_VIM_LXC)['data']['status'] == 'stopped':
    # start up the vm
    PROX_CONNECTION.com_net_prox_node_lxc_start('pve', JENKINS_BUILD_UBUNTU_VIM_LXC)
    time.sleep(120) # wait two minutes for box to boot


# connect to server via ssh
SSH_BUILD = common_network_ssh.CommonNetworkSSH(JENKINS_BUILD_UBUNTU_VIM_LNX_IP,\
    'metaman', 'metaman')

# TODO rollback snap to base?

# begin build of deps
SSH_BUILD.com_net_ssh_run_sudo_command('sudo apt-get update')
# auto yes to accept install
# this list at the moment is for building pip install
SSH_BUILD.com_net_ssh_run_sudo_command('sudo apt-get -y install autoconf automake'\
    ' build-essential libass-dev upx-ucl sshpass libjpeg-dev'\
    ' libfreetype6-dev libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev'\
    ' libvorbis-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev pkg-config texinfo'\
    ' zlib1g-dev yasm cmake git curl wget libsmbclient-dev python-pip postgresql-server-dev-9.5'\
    ' libffi-dev libsnmp-dev libldap2-dev libsasl2-dev portaudio19-dev')
# setup pip and pyinstaller
SSH_BUILD.com_net_ssh_run_sudo_command('sudo pip install --upgrade pip')
SSH_BUILD.com_net_ssh_run_sudo_command('sudo pip install pyinstaller')
SSH_BUILD.com_net_ssh_run_sudo_command('sudo pip install -r /home/metaman/MediaKraken_Deployment/'\
    'build_code/jenkins/pipeline-build-os/pipeline-build-os-pip-server-ubuntu.txt')
# should fix pyopenssl error
SSH_BUILD.com_net_ssh_run_sudo_command('sudo pip install requests[security]')


# TODO easy_install zope.interface  didn't fix

# git pull down latest stage/RC code branch
SSH_BUILD.com_net_ssh_run_command('cd /home/metaman')
if os.path.isdir('/home/metaman/MediaKraken_Deployment'):
    SSH_BUILD.com_net_ssh_run_command('cd MediaKraken_Deployment')
    SSH_BUILD.com_net_ssh_run_command('git pull --recurse-submodules')
else:
    SSH_BUILD.com_net_ssh_run_command('git clone --recursive -b '\
                                      + FFMPEG_BRANCH + ' https://github.com/'\
                                      'MediaKraken/MediaKraken_Deployment')
    SSH_BUILD.com_net_ssh_run_command('cd MediaKraken_Deployment')
# setup branch
SSH_BUILD.com_net_ssh_run_command('cd MediaKraken_Build')
SSH_BUILD.com_net_ssh_run_command('git checkout %s' % FFMPEG_BRANCH)
SSH_BUILD.com_net_ssh_run_command('cd ..')


## git pull down latest master
#SSH_BUILD.com_net_ssh_run_command('cd /home/metaman')
#if os.path.isdir('/home/metaman/MediaKraken_Submodules'):
#    SSH_BUILD.com_net_ssh_run_command('cd MediaKraken_Submodules')
#    SSH_BUILD.com_net_ssh_run_command('git pull --recurse-submodules')
#else:
#    SSH_BUILD.com_net_ssh_run_command('git clone --recursive https://github.com/'\
#        'MediaKraken/MediaKraken_Submodules')


# build ffmpeg
SSH_BUILD.com_net_ssh_run_command('/home/metaman/MediaKraken_Deployment/build_code/jenkins'\
    '/pipeline-build-os/pipeline-build-os-ubuntu-ffmpeg.sh')


SSH_BUILD.com_net_ssh_close()
