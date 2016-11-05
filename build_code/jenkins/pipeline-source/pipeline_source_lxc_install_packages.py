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
import os
import sys
sys.path.append('.')
sys.path.append('../MediaKraken-PyLint') # for jenkins server
from common import common_network_ssh
import pipeline_source_lxc_definitions
import pipeline_source_packages_ubuntu

# build the containers if not already exist
for server_info in pipeline_source_lxc_definitions.SERVERS_TO_BUILD:
    print('server: %s' % str(server_info))
    command_string = ''
    # check to verify it needs to build lxc
    if server_info[1] == True and server_info[6] is not None:
        if server_info[3] == 'ubuntu' or server_info[3] == 'debian':
            command_string += 'sudo apt-get -y install '
        elif server_info[3] == 'alpine':
            command_string += 'apk add '
        # loop through commands and build install string
        for package_name in pipeline_source_packages_ubuntu.PACKAGES_BASE_UBUNTU_1604:
            command_string += package_name + ' '
        for package_name in server_info[4]:
            command_string += package_name + ' '
        command_string = command_string.strip()
        # connect to server via ssh
        SSH_BUILD = common_network_ssh.CommonNetworkSSH(server_info[6], 'metaman', 'metaman')
        SSH_BUILD.com_net_ssh_run_sudo_command('sudo apt-get update')
        SSH_BUILD.com_net_ssh_run_sudo_command(command_string)
        if server_info[7] is not None:
            SSH_BUILD.com_net_ssh_run_sudo_command('sudo pip install --upgrade pip')
            # xfer pip file
            os.system('sudo sshpass -p \'metaman\''\
                ' scp -r -o StrictHostKeyChecking=no ./build_code/jenkins/pipeline-source/%s'\
                ' metaman@%s:/home/metaman/.' % (server_info[7], server_info[6]))
            # run/install the pip packages
            SSH_BUILD.com_net_ssh_run_sudo_command('sudo pip install --upgrade -r %s'\
                % server_info[5])
            SSH_BUILD.com_net_ssh_run_sudo_command('rm %s' % server_info[5])
        if server_info[0].find('FFMPEG') != -1:
            # fire off build ffmpeg
            os.system('sudo sshpass -p \'metaman\''\
                ' scp -r -o StrictHostKeyChecking=no ./build_code/jenkins/pipeline-source/%s'\
                ' metaman@%s:/home/metaman/.' % (server_info[5], server_info[6]))
            SSH_BUILD_FFMPEG = common_network_ssh.CommonNetworkSSH(server_info[6],\
                                                                   'metaman', 'metaman')
            SSH_BUILD_FFMPEG.com_net_ssh_run_sudo_command('sudo ./%s' % server_info[5])
            SSH_BUILD_FFMPEG.com_net_ssh_close()
        else:
            # setup directories needed for app
            SSH_BUILD.com_net_ssh_run_command('mkdir mediakraken')
            SSH_BUILD.com_net_ssh_run_command('mkdir mediakraken/bin')
            SSH_BUILD.com_net_ssh_run_command('mkdir mediakraken/cache')
            SSH_BUILD.com_net_ssh_run_command('mkdir mediakraken/conf')
            SSH_BUILD.com_net_ssh_run_command('mkdir mediakraken/key')
            SSH_BUILD.com_net_ssh_run_command('mkdir mediakraken/log')
            # it's setup for server....so more directories
            if server_info[0].find('Server') != -1:
                SSH_BUILD.com_net_ssh_run_command('mkdir mediakraken/backups')
                SSH_BUILD.com_net_ssh_run_command('mkdir mediakraken/passwordmeter')
                SSH_BUILD.com_net_ssh_run_command('mkdir mediakraken/passwordmeter/res')
                # as server more code needed
                for folder_name in ('database', 'metadata', 'network', 'web_app'):
                    os.system('sudo sshpass -p \'metaman\''\
                        ' scp -r -o StrictHostKeyChecking=no ./%s'\
                        ' metaman@%s:/home/metaman/mediakraken/.' % (folder_name, server_info[6]))
                # main server programs
                for program_name in ('bulk_gamesdb_netfetch.py', 'main_server.py',\
                        'main_server_api.py', 'main_server_link.py',\
                        'main_server_metadata_api.py',\
                        'main_server_trigger.py'):
                    os.system('sudo sshpass -p \'metaman\''\
                        ' scp -r -o StrictHostKeyChecking=no ./%s'\
                        ' metaman@%s:/home/metaman/mediakraken/.' % (program_name, server_info[6]))
                # subprograms
                os.system('sudo sshpass -p \'metaman\''\
                    ' scp -r -o StrictHostKeyChecking=no ./subprogram*.py'\
                    ' metaman@%s:/home/metaman/mediakraken/.' % server_info[6])
                # ini config
                os.system('sudo sshpass -p \'metaman\''\
                    ' scp -r -o StrictHostKeyChecking=no ./MediaKraken.ini'\
                    ' metaman@%s:/home/metaman/mediakraken/.' % server_info[6])
                # install calibre binaries for ebook conversion support
                SSH_BUILD.com_net_ssh_run_command("wget -nv -O- https://raw.githubusercontent.com/kovidgoyal/calibre/master/setup/linux-installer.py | python -c \"import sys; main=lambda x,y:sys.stderr.write('Download failed'); exec(sys.stdin.read()); main('/home/metaman/mediakraken/bin', True)\"")
            else:
                # move only slave programs
                os.system('sudo sshpass -p \'metaman\''\
                    ' scp -r -o StrictHostKeyChecking=no ./main_server_slave.py'\
                    ' metaman@%s:/home/metaman/mediakraken/.' % server_info[6])
                # ini config
                os.system('sudo sshpass -p \'metaman\''\
                    ' scp -r -o StrictHostKeyChecking=no ./MediaKraken_Slave.ini'\
                    ' metaman@%s:/home/metaman/mediakraken/.' % server_info[6])
            # move rest of server/slave code
            # ffmpeg bins
            # TODO!!!!!!!!
            for folder_name in ('common', 'conf'):
                os.system('sudo sshpass -p \'metaman\''\
                    ' scp -r -o StrictHostKeyChecking=no ./%s'\
                    ' metaman@%s:/home/metaman/mediakraken/.' % (folder_name, server_info[6]))
            # rest of general files
            for file_name in ('README.md', 'LICENSE'):
                os.system('sudo sshpass -p \'metaman\''\
                    ' scp -r -o StrictHostKeyChecking=no ./%s'\
                    ' metaman@%s:/home/metaman/mediakraken/.' % (file_name, server_info[6]))
        # close connection to this server
        SSH_BUILD.com_net_ssh_close()
