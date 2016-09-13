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
JENKINS_DEPLOY_UBUNTU_VIM_LNX_IP = '10.0.0.166'


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
SSH_DEPLOY.com_net_ssh_run_sudo_command('sudo apt-get -y install postgresql ffmpeg'\
    ' libva-drm1 libva-x11-1 libsmbclient')
# scp ffmpeg
SSH_BUILD.com_net_ssh_run_sudo_command('sudo sshpass -p \'metaman\''\
    ' scp -o StrictHostKeyChecking=no /home/metaman/bin/ff*'\
    ' metaman@10.0.0.166:/home/metaman/.')
SSH_DEPLOY.com_net_ssh_run_sudo_command('sudo mv /home/metaman/ff* /usr/bin/.')
SSH_DEPLOY.com_net_ssh_run_sudo_command('sudo ldconfig')

# prep files to scp
SSH_BUILD.com_net_ssh_run_command('mkdir /home/metaman/dist/xfer')
SSH_BUILD.com_net_ssh_run_command('rm -Rf /home/metaman/dist/xfer/*')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/main_server/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/main_server_api/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/main_server_link/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/main_server_metadata_api/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/main_server_slave/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/main_server_trigger/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_broadcast/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_chromecast_discover/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_commercial_strip/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_create_chapter_images/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_cron_checker/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_ffmpeg_process/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_file_scan/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_game_audit/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_game_metadata_giantbomb/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_game_metadata_igdb/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_iradio_channels/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_livestream_downloader/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_logo_download/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_lyrics_downloader/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_match_anime_id_scudlee/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_musicbrainz_sync/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_postgresql_backup/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_postgresql_vacuum/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_reactor_string_weblog/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_reactor_string/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_reactor_web_images/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_roku_thumbnail_generate/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_schedules_direct_updates/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_ssl_keygen/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_subtitle_downloader/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_sync/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_thetvdb_images/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_thetvdb_updates/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_tuner_discover/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_tvmaze_images/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_tvmaze_updates/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_update_create_collections/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_url_checker/ /home/metaman/dist/xfer/.')
SSH_BUILD.com_net_ssh_run_command(\
    'rsync -r /home/metaman/dist/subprogram_zfs_check/ /home/metaman/dist/xfer/.')

# scp actual programs
SSH_BUILD.com_net_ssh_run_sudo_command('sudo sshpass -p \'metaman\''\
    ' scp -r -o StrictHostKeyChecking=no /home/metaman/dist/xfer/*'\
    ' metaman@%s:/home/metaman/mediakraken/.' % JENKINS_DEPLOY_UBUNTU_VIM_LNX_IP)

# scp the password common
SSH_BUILD.com_net_ssh_run_sudo_command('sudo sshpass -p \'metaman\''\
    ' scp -r -o StrictHostKeyChecking=no /home/metaman/MediaKraken_Submodules/passwordmeter/'\
    'passwordmeter/res/common.txt'\
    ' metaman@%s:/home/metaman/mediakraken/passwordmeter/res/.' % JENKINS_DEPLOY_UBUNTU_VIM_LNX_IP)

# copy over config files
SSH_BUILD.com_net_ssh_run_sudo_command('sudo sshpass -p \'metaman\''\
    ' scp -o StrictHostKeyChecking=no /home/metaman/MediaKraken_Deployment/'\
    'MediaKraken.ini metaman@%s:/home/metaman/mediakraken/.' % JENKINS_DEPLOY_UBUNTU_VIM_LNX_IP)

# copy postgresl user file
SSH_BUILD.com_net_ssh_run_sudo_command('sudo sshpass -p \'metaman\''\
    ' scp -o StrictHostKeyChecking=no /home/metaman/MediaKraken_Deployment/'\
    'MediaKraken_Build/jenkins/pipeline-deploy-os/pipeline-deploy-os-server-ubuntu-pgsql-user.sh'\
    ' metaman@%s:/home/metaman/mediakraken/.' % JENKINS_DEPLOY_UBUNTU_VIM_LNX_IP)
# create the postgresql user
SSH_DEPLOY.com_net_ssh_run_sudo_command('sudo /home/metaman/mediakraken/'\
    'pipeline-deploy-os-server-ubuntu-pgsql-user.sh')
# remove user create script
SSH_DEPLOY.com_net_ssh_run_command('rm /home/metaman/mediakraken/'\
    'pipeline-deploy-os-server-ubuntu-pgsql-user.sh')

# copy ffmpeg and libs
SSH_BUILD.com_net_ssh_run_sudo_command('sudo sshpass -p \'metaman\''\
    ' scp -o StrictHostKeyChecking=no /home/metaman/bin/*'\
    ' metaman@%s:/home/metaman/mediakraken/bin/.' % JENKINS_DEPLOY_UBUNTU_VIM_LNX_IP)

SSH_DEPLOY.com_net_ssh_close()
SSH_BUILD.com_net_ssh_close()
