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
from common import common_network_vm_proxmox
import pipeline_source_lxc_definitions


# create prox class instance to use
PROX_CONNECTION = common_network_vm_proxmox.CommonNetworkProxMox('10.0.0.190', 'root@pam',\
    'jenkinsbuild')


# build the containers if not already exist
lxc_dict = {}
for lxc_server in PROX_CONNECTION.com_net_prox_node_lxc_list('pve')['data']:
    lxc_dict[lxc_server['name']] = (lxc_server['vmid'], lxc_server['status'])
print('lxc: %s' % lxc_dict)
for server_info in pipeline_source_lxc_definitions.SERVERS_TO_BUILD:
    print('server: %s' % str(server_info))
    # check to verify it needs to build lxc
    if server_info[1] == True:
        # if server already built
        if server_info[0] in lxc_dict:
            print('status: %s' % str(lxc_dict[server_info[0]][1]))
            # make sure it's started
            if lxc_dict[server_info[0]] != 'running':
                # start up the vm
                print('start vim: %s' % lxc_dict[server_info[0]][0])
                print(PROX_CONNECTION.com_net_prox_node_lxc_start(\
                    'pve', lxc_dict[server_info[0]][0]))
        else:
            print('create server: %s' % str(server_info[2]))
            print(PROX_CONNECTION.com_net_prox_node_lxc_create('pve', server_info[0], 4096,\
                                                               server_info[2], 'ZFSthin',\
                                                               server_info[3]))

## keep an eye on task and see when its completed
#while node.tasks(taskid).status()['status'] == 'running':
#        time.sleep(1)
