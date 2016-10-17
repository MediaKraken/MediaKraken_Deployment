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
# Will be used to build the deps like FFMPEG
###
JENKINS_BUILD_UBUNTU_VIM_LXC = 104
JENKINS_BUILD_UBUNTU_VIM_LNX_IP = '10.0.0.135'
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

# Don't build single file apps......as then it's alot of dupelicate imports
# Don't build single file apps......as then it's alot of dupelicate imports
# Don't build single file apps......as then it's alot of dupelicate imports
# Don't build single file apps......as then it's alot of dupelicate imports

# nuke previous pyinstaller directories to start fresh
SSH_BUILD.com_net_ssh_run_command('rm -Rf /home/metaman/build')
SSH_BUILD.com_net_ssh_run_command('rm -Rf /home/metaman/dist')

# start building python "app"
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/main_server.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/main_server_api.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/main_server_link.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/main_server_metadata_api.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/main_server_slave.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/main_server_trigger.py')

# start building the subprograms
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_broadcast.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_chromecast_discover.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_commercial_strip.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_create_chapter_images.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_cron_checker.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_file_scan.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_game_audit.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_game_metadata_giantbomb.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_game_metadata_igdb.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_iradio_channels.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_livestream_downloader.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_logo_download.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_lyrics_downloader.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_match_anime_id_scudlee.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_metadata_musicbrainz_sync.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_postgresql_backup.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_postgresql_vacuum.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_reactor_string_weblog.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_reactor_string.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_reactor_web_images.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_roku_thumbnail_generate.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_schedules_direct_updates.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_ssl_keygen.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_metadata_subtitle_downloader.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_sync.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_metadata_thetvdb_images.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_metadata_thetvdb_updates.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_tuner_discover.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_metadata_tvmaze_images.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_metadata_tvmaze_updates.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_metadata_update_create_collections.py')
SSH_BUILD.com_net_ssh_run_command('pyinstaller --clean'\
    ' /home/metaman/MediaKraken_Deployment/subprogram_zfs_check.py')


SSH_BUILD.com_net_ssh_close()
