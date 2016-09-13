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
from common import common_network_ssh
from common import common_network_vm_proxmox


###
# Will be used to deploy ubuntu server
###
JENKINS_BUILD_UBUNTU_VIM_LXC = 108
JENKINS_BUILD_UBUNTU_VIM_LNX_IP = '10.0.0.153'
JENKINS_DEPLOY_UBUNTU_VIM_LXC = 106
JENKINS_DEPLOY_UBUNTU_VIM_LNX_IP = '10.0.0.183'


# create prox class instance to use
PROX_CONNECTION = common_network_vm_proxmox.CommonNetworkProxMox('10.0.0.190', 'root@pam',\
    'jenkinsbuild')


# check status of ubuntu build vm
if PROX_CONNECTION.com_net_prox_node_lxc_status('pve',\
        JENKINS_BUILD_UBUNTU_VIM_LXC)['data']['status'] == 'stopped':
    # start up the vm
    PROX_CONNECTION.com_net_prox_node_lxc_start('pve', JENKINS_BUILD_UBUNTU_VIM_LXC)
    time.sleep(120) # wait two minutes for box to boot


# check status of ubuntu deploy vm
if PROX_CONNECTION.com_net_prox_node_lxc_status('pve',\
        JENKINS_DEPLOY_UBUNTU_VIM_LXC)['data']['status'] == 'stopped':
    # start up the vm
    PROX_CONNECTION.com_net_prox_node_lxc_start('pve', JENKINS_DEPLOY_UBUNTU_VIM_LXC)
    time.sleep(120) # wait two minutes for box to boot


# connect to server via ssh
SSH_DEPLOY = common_network_ssh.CommonNetworkSSH(JENKINS_DEPLOY_UBUNTU_VIM_LNX_IP,\
    'metaman', 'metaman')

SSH_BUILD = common_network_ssh.CommonNetworkSSH(JENKINS_BUILD_UBUNTU_VIM_LNX_IP,\
    'metaman', 'metaman')


# TODO rollback snap to base?

# setup directories needed for app
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/bin')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/cache')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/conf')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/log')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/passwordmeter')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/passwordmeter/res')
SSH_DEPLOY.com_net_ssh_run_command('cd mediakraken')

# install servers deps
SSH_DEPLOY.com_net_ssh_run_sudo_command('setup-xorg-base')
SSH_DEPLOY.com_net_ssh_run_sudo_command('apk add xfce4')
apk add xf86-video-modesetting
apk add xf86-input-mouse xf86-input-keyboard
Xorg -configure
rc-service dbus start
rc-update add dbus

apk add nano
nano /etc/apk/repositories
1. Un-comment the community in the repositories
apk update
apk add alpine-desktop

rc-service lxdm start
## scp ffmpeg
#SSH_BUILD.com_net_ssh_run_sudo_command('sudo sshpass -p \'metaman\''\
#    ' scp -o StrictHostKeyChecking=no /home/metaman/bin/ff*'\
#    ' metaman@10.0.0.166:/home/metaman/.')
#SSH_DEPLOY.com_net_ssh_run_sudo_command('sudo mv /home/metaman/ff* /usr/bin/.')
#SSH_DEPLOY.com_net_ssh_run_sudo_command('sudo ldconfig')

SSH_DEPLOY.com_net_ssh_close()
SSH_BUILD.com_net_ssh_close()
