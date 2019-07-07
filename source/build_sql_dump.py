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

import subprocess

from common import common_network_ssh

# # start the postgres if not up on pve
# prox_inst = common_network_vm_proxmox.CommonNetworkProxMox('pve', 'metaman', 'metaman')
# if prox_inst.com_net_prox_api_connect() is None:
#     print('Error connecting to Proxmox!!')
#     sys.exit(0)
#
# # go through the node(s) in a cluster
# for node_name in prox_inst.com_net_prox_cluster_config_nodes():
#     print(node_name)
#     # list vm's
#     for kvm_list in prox_inst.com_net_prox_node_qemu_list('pve'):
#         print(kvm_list)
#         if blah == blah:
#             node = blah
#             vmid = blah
#             break
#
#     # list containers
#     for lxc_list in prox_inst.com_net_prox_node_lxc_list('pve'):
#         print(lxc_list)
#         if blah == blah:
#             node = blah
#             vmid = blah
#             break
#
# # start the vm from selected machine above
# vm_status = prox_inst.com_net_prox_node_lxc_status(node, vmid)
# if vm_status == 'off':
#     prox_inst.com_net_prox_node_lxc_start(node, vmid)
#     time.sleep(60)

# log into the postgresql vm
ssh_inst = common_network_ssh.CommonNetworkSSH('th-postgresql-1', 'metaman', 'metaman')

# drop the db, this name can be this even with user specified as the db name
# is not in the dump file
ssh_inst.com_net_ssh_run_sudo_command('psql -U postgres -c "drop database metamandb"')

# create the empty database
ssh_inst.com_net_ssh_run_sudo_command('psql -U postgres -c "create database metamandb"')

# enable pg_trgm
ssh_inst.com_net_ssh_run_sudo_command(
    'psql -U postgres -d metamandb -c "create extension pg_trgm;"')

db_create_pid = subprocess.Popen(['python3',
                                  '/home/metaman/MediaKraken_Deployment/source/db_create_update.py'],
                                 stdout=subprocess.PIPE, shell=False)
db_create_pid.wait()

# do a dump which defaults to plain text
ssh_inst.com_net_ssh_run_sudo_command(
    'pg_dump -U postgres -d metamandb -f /home/metaman/create_schema.sql')

# close the ssh connection
ssh_inst.com_net_ssh_close()

# scp the file to local machine
scp_inst = subprocess.Popen(['scp', '-r', 'metaman@th-postgresql-1:/home/metaman/create_schema.sql',
                             '../docker/alpine/ComposeMediaKrakenDatabase/docker-entrypoint-initdb.d/.'],
                            stdout=subprocess.PIPE, shell=False)
scp_inst.wait()
