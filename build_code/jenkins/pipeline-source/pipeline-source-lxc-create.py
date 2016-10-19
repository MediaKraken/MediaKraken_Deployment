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
from common import common_network_vm_proxmox


BUILD_BRANCH = 'dev-0.1.11'
SERVERS_TO_BUILD = [
    # VM name, Build lxc, image, package list
    ('SourceAlpine33', False, 'imagetouse', packagelist),
    ('SourceAlpine34', False, 'imagetouse', packagelist),
    ('SourceDebian84', False, 'imagetouse', packagelist),
    ('SourceDebian85', False, 'imagetouse', packagelist),
    ('SourceDebian86', False, 'imagetouse', packagelist),
    ('SourceUbuntu1504', False, 'imagetouse', packagelist),
    ('SourceUbuntu1510', False, 'imagetouse', packagelist),
    ('SourceUbuntu1604', True, 'imagetouse', packagelist),
    ]


# create prox class instance to use
PROX_CONNECTION = common_network_vm_proxmox.CommonNetworkProxMox('10.0.0.190', 'root@pam',\
    'jenkinsbuild')


# build the containers if not already exist
lxc_list = PROX_CONNECTION.com_net_prox_node_lxc_list('pve')
for server_info in SERVERS_TO_BUILD:
    # if server already built
    if server_info[0] in lxc_list:
        # make sure it's started
        if PROX_CONNECTION.com_net_prox_node_lxc_status('pve',\
                JENKINS_BUILD_SOURCE_VIM_LXC)['data']['status'] == 'stopped':
            # start up the vm
            PROX_CONNECTION.com_net_prox_node_lxc_start('pve', JENKINS_BUILD_SOURCE_VIM_LXC)
    else:
        # check to verify it needs to build lxc
        if server_info[1] == True:
            pass




# keep an eye on task and see when its completed
while node.tasks(taskid).status()['status'] == 'running':
        time.sleep(1)
