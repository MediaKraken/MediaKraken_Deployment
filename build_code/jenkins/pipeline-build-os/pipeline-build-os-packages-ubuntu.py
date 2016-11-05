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
import time
import sys
sys.path.append('.')
sys.path.append('../MediaKraken-PyLint') # for jenkins server
sys.path.append('../MediaKraken-PyLint/build_code/jenkins/')
import pipeline_packages_list
from common import common_network_ssh
from common import common_network_vm_proxmox


###
# Will be used to build the deps like FFMPEG
###
JENKINS_BUILD_UBUNTU_VIM_LXC = 108
JENKINS_BUILD_UBUNTU_VIM_LNX_IP = '10.0.0.153'
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


# nuke previous pyinstaller directories to start fresh
SSH_BUILD.com_net_ssh_run_command('rm -Rf /home/metaman/build')
SSH_BUILD.com_net_ssh_run_command('rm -Rf /home/metaman/dist')

# start building python programs
for app_to_build in pipeline_packages_list.PIPELINE_APP_LIST:
    SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
                                      ' /home/metaman/MediaKraken_Deployment/'\
                                      + app_to_build + '.py')


SSH_BUILD.com_net_ssh_close()
