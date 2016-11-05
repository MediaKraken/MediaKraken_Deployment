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
# Will be used to deploy ubuntu server
###
JENKINS_BUILD_VIM_LXC = 104
JENKINS_BUILD_VIM_LNX_IP = '10.0.0.135'
JENKINS_DEPLOY_VIM_LXC = 112
JENKINS_DEPLOY_VIM_LNX_IP = '10.0.0.123'


# create prox class instance to use
PROX_CONNECTION = common_network_vm_proxmox.CommonNetworkProxMox('10.0.0.190', 'root@pam',\
    'jenkinsbuild')


# check status of ubuntu build vm
if PROX_CONNECTION.com_net_prox_node_lxc_status('pve',\
        JENKINS_BUILD_VIM_LXC)['data']['status'] == 'stopped':
    # start up the vm
    PROX_CONNECTION.com_net_prox_node_lxc_start('pve', JENKINS_BUILD_VIM_LXC)
    time.sleep(120) # wait two minutes for box to boot


# check status of ubuntu deploy vm
if PROX_CONNECTION.com_net_prox_node_lxc_status('pve',\
        JENKINS_DEPLOY_VIM_LXC)['data']['status'] == 'stopped':
    # start up the vm
    PROX_CONNECTION.com_net_prox_node_lxc_start('pve', JENKINS_DEPLOY_VIM_LXC)
    time.sleep(120) # wait two minutes for box to boot


# connect to server via ssh
SSH_DEPLOY = common_network_ssh.CommonNetworkSSH(JENKINS_DEPLOY_VIM_LNX_IP,\
    'metaman', 'metaman')

SSH_BUILD = common_network_ssh.CommonNetworkSSH(JENKINS_BUILD_VIM_LNX_IP,\
    'metaman', 'metaman')


# TODO rollback snap to base?

# setup directories needed for app
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/backups')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/bin')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/cache')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/conf')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/key')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/log')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/passwordmeter')
SSH_DEPLOY.com_net_ssh_run_command('mkdir mediakraken/passwordmeter/res')
SSH_DEPLOY.com_net_ssh_run_command('cd mediakraken')

# install servers deps
# way too many deps, so install ffmpeg to stomp over with compiled version
SSH_DEPLOY.com_net_ssh_run_command('apt-get -y install postgresql ffmpeg'\
    ' libva-drm1 libva-x11-1 libsmbclient nfs-common nginx redis-server'\
    ' cifs-utils')



# libhdhomerun



# scp ffmpeg
SSH_BUILD.com_net_ssh_run_command('sshpass -p \'metaman\''\
    ' scp -o StrictHostKeyChecking=no /home/metaman/bin/ff*'\
    ' metaman@%s:/home/metaman/.' % JENKINS_DEPLOY_VIM_LNX_IP)
SSH_DEPLOY.com_net_ssh_run_command('mv /home/metaman/ff* /usr/bin/.')
SSH_DEPLOY.com_net_ssh_run_command('ldconfig')

# prep files to scp
SSH_BUILD.com_net_ssh_run_command('mkdir /home/metaman/dist/xfer')
SSH_BUILD.com_net_ssh_run_command('rm -Rf /home/metaman/dist/xfer/*')

# move all programs
for app_to_build in pipeline_packages_list.PIPELINE_APP_LIST:
    SSH_BUILD.com_net_ssh_run_command('rsync -r /home/metaman/dist/' + app_to_build\
                                      + '/ /home/metaman/dist/xfer/.')

# scp actual programs
SSH_BUILD.com_net_ssh_run_command('sshpass -p \'metaman\''\
    ' scp -r -o StrictHostKeyChecking=no /home/metaman/dist/xfer/*'\
    ' metaman@%s:/home/metaman/mediakraken/.' % JENKINS_DEPLOY_VIM_LNX_IP)

# scp the password common
SSH_BUILD.com_net_ssh_run_command('sshpass -p \'metaman\''\
    ' scp -r -o StrictHostKeyChecking=no /home/metaman/MediaKraken_Submodules/passwordmeter/'\
    'passwordmeter/res/common.txt'\
    ' metaman@%s:/home/metaman/mediakraken/passwordmeter/res/.' % JENKINS_DEPLOY_VIM_LNX_IP)

# copy over config files
SSH_BUILD.com_net_ssh_run_command('sshpass -p \'metaman\''\
    ' scp -o StrictHostKeyChecking=no /home/metaman/MediaKraken_Deployment/'\
    'MediaKraken.ini metaman@%s:/home/metaman/mediakraken/.' % JENKINS_DEPLOY_VIM_LNX_IP)

# copy postgresl user file
SSH_BUILD.com_net_ssh_run_command('sshpass -p \'metaman\''\
    ' scp -o StrictHostKeyChecking=no /home/metaman/MediaKraken_Deployment/'\
    'build_code/jenkins/pipeline-deploy-os/pipeline-deploy-os-server-pgsql-user-debian.sh'\
    ' metaman@%s:/home/metaman/mediakraken/.' % JENKINS_DEPLOY_VIM_LNX_IP)

# create the postgresql user
SSH_DEPLOY.com_net_ssh_run_command('/home/metaman/mediakraken/'\
    'pipeline-deploy-os-server-ubuntu-pgsql-user.sh')

# remove user create script
SSH_DEPLOY.com_net_ssh_run_command('rm /home/metaman/mediakraken/'\
    'pipeline-deploy-os-server-pgsql-user-debian.sh')

# copy ffmpeg and libs
SSH_BUILD.com_net_ssh_run_command('sshpass -p \'metaman\''\
    ' scp -o StrictHostKeyChecking=no /home/metaman/bin/*'\
    ' metaman@%s:/home/metaman/mediakraken/bin/.' % JENKINS_DEPLOY_VIM_LNX_IP)

SSH_DEPLOY.com_net_ssh_close()
SSH_BUILD.com_net_ssh_close()
