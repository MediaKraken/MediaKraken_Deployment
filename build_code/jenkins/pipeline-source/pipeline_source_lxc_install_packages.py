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
import sys
sys.path.append('.')
sys.path.append('../MediaKraken-PyLint') # for jenkins server
from common import common_network_ssh
import pipeline_source_lxc_definitions


# build the containers if not already exist
for server_info in pipeline_source_lxc_definitions.SERVERS_TO_BUILD:
    print('server: %s' % str(server_info))
    command_string = ''
    pip_string = 'pip install --upgrade '
    # check to verify it needs to build lxc
    if server_info[1] == True:
        if server_info[3] == 'ubuntu' or server_info[3] == 'debian':
            command_string += 'sudo apt-get -y install '
            pip_string = 'sudo ' + pip_string
        elif server_info[3] == 'alpine':
            command_string += 'apk add '
        # loop through commands and build install string
        for package_name in server_info[4]:
            command_string += package_name + ' '
        command_string = command_string.strip()
        # loop through pip and build install string
        for pip_name in server_info[5]:
            pip_string += pip_name + ' '
        # connect to server via ssh
        SSH_BUILD = common_network_ssh.CommonNetworkSSH('10.0.0.109', 'metaman', 'metaman')
        SSH_BUILD.com_net_ssh_run_sudo_command('sudo apt-get update')
        SSH_BUILD.com_net_ssh_run_sudo_command(command_string)
        SSH_BUILD.com_net_ssh_run_sudo_command(pip_string)
        # close connection to this server
        SSH_BUILD.com_net_ssh_close()
