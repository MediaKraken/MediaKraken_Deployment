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
import requests


class CommonNetworkProxMox(object):
    """
    Class for interfacing via proxmox
    """
    def __init__(self, node_addr, node_user, node_password):
        self.httpheaders = {'Accept': 'application/json',\
            'Content-Type': 'application/x-www-form-urlencoded'}
        self.full_url = ('https://%s:8006/api2/json/' % node_addr)
        api_response = requests.post(self.full_url + 'access/ticket', verify=False,\
            data={'username': node_user, 'password': node_password}).json()
        self.prox_ticket = {'PVEAuthCookie': api_response['data']['ticket']}
        self.httpheaders['CSRFPreventionToken'] = str(api_response['data']['CSRFPreventionToken'])


    def com_net_prox_api_call(self, request_type, api_call_type, post_data=None):
        """
        Do api call to specified connection
        """
        if request_type == "get":
            return requests.get(self.full_url + api_call_type, verify=False,
                                cookies=self.prox_ticket).json()
        else:
            return requests.post(self.full_url + api_call_type, verify=False,
                                 data=post_data,
                                 cookies=self.prox_ticket,
                                 headers=self.httpheaders).json()

    ###
    # Access API
    ###
    def com_net_prox_access(self):
        """
        Directory index.
        """
        return self.com_net_prox_api_call('get', 'access')

    ###
    # Access/domains API
    ###


    ###
    # Access/groups API
    ###


    ###
    # Access/roles API
    ###


    ###
    # Access/users API
    ###


    ###
    # Access/acl API
    ###


    ###
    # Access/password API
    ###


    ###
    # Access/ticket API
    ###


    ###
    # Cluster API
    ###
    def com_net_prox_cluster_ndx(self):
        """
        Get the index of the cluster
        """
        return self.com_net_prox_api_call('get', 'cluster')


    ###
    # Cluster/backup API
    ###
    def com_net_prox_cluster_backup(self):
        """
        Get the backup list of the cluster
        """
        return self.com_net_prox_api_call('get', 'cluster/backup')


    ###
    # Cluster/firewall API
    ###


    ###
    # Cluster/ha API
    ###


    ###
    # Cluster/log API
    ###


    ###
    # Cluster/nextid API
    ###


    ###
    # Cluster/options API
    ###


    ###
    # Cluster/resources API
    ###


    ###
    # Cluster/status API
    ###
    def com_net_prox_cluster_status(self):
        """
        Get the status of the cluster
        """
        return self.com_net_prox_api_call('get', 'cluster/status')


    ###
    # Cluster/tasks API
    ###


    ###
    # Nodes
    ###
    def com_net_prox_node_index(self,):
        """
        Cluster node index.
        """
        return self.com_net_prox_api_call('get', 'nodes')


    ###
    # Nodes/apt
    ###


    ###
    # Nodes/ceph
    ###


    ###
    # Nodes/firewall
    ###


    ###
    # Nodes/lxc
    ###
    def com_net_prox_node_lxc_list(self, node_name):
        """
        Get a list of the lxc vms on node
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/lxc' % node_name)


    def com_net_prox_node_lxc_status(self, node_name, vm_id):
        """
        Get a status of the lxc vm
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/lxc/%s/status/current'\
            % (node_name, vm_id))


    def com_net_prox_node_lxc_start(self, node_name, vm_id):
        """
        Start lxc vm
        """
        return self.com_net_prox_api_call('post', 'nodes/%s/lxc/%s/status/start'\
            % (node_name, vm_id))


    def com_net_prox_node_lxc_stop(self, node_name, vm_id):
        """
        Stop lxc vm
        """
        return self.com_net_prox_api_call('post', 'nodes/%s/lxc/%s/status/stop'\
            % (node_name, vm_id))


    def com_net_prox_node_lxc_snaps(self, node_name, vm_id):
        """
        List snaps for lxc vm
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/lxc/%s/snapshot'\
            % (node_name, vm_id))


    def com_net_prox_node_lxc_clone(self, node_name, vm_id, post_data_json):
        """
       Create clone for lxc vm
        """
        return self.com_net_prox_api_call('post', 'nodes/%s/lxc/%s/clone'\
            % (node_name, vm_id), post_data_json)


    ###
    # Nodes/network
    ###


    ###
    # Nodes/qemu
    ###
    def com_net_prox_node_qemu_list(self, node_name):
        """
        Get a list of the qemu vms on node
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/qemu' % node_name)


    def com_net_prox_node_qemu_status(self, node_name, vm_id):
        """
        Get a status of the qemu vm
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/qemu/%s/status/current'\
            % (node_name, vm_id))


    def com_net_prox_node_qemu_start(self, node_name, vm_id):
        """
        Start qemu vm
        """
        return self.com_net_prox_api_call('post', 'nodes/%s/qemu/%s/status/start'\
            % (node_name, vm_id))


    def com_net_prox_node_qemu_stop(self, node_name, vm_id):
        """
        Stop qemu vm
        """
        return self.com_net_prox_api_call('post', 'nodes/%s/qemu/%s/status/stop'\
            % (node_name, vm_id))


    def com_net_prox_node_qemu_snaps(self, node_name, vm_id):
        """
        List snaps for qemu vm
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/qemu/%s/snapshot'\
            % (node_name, vm_id))


    def com_net_prox_node_qemu_clone(self, node_name, vm_id, post_data_json):
        """
       Create clone for qemu vm
        """
        return self.com_net_prox_api_call('post', 'nodes/%s/qemu/%s/clone'\
            % (node_name, vm_id), post_data_json)


    ###
    # Nodes/scan
    ###


    ###
    # Nodes/services
    ###


    ###
    # Nodes/storage
    ###


    ###
    # Nodes/tasks
    ###


    ###
    # Nodes/aplinfo
    ###


    ###
    # Nodes/dns
    ###


    ###
    # Nodes/execute
    ###


    ###
    # Nodes/migreateall
    ###


    ###
    # Nodes/netstat
    ###
    def com_net_prox_node_netstat(self, node_name):
        """
        Get a network device counters of node
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/netstat' % node_name)


    ###
    # Nodes/report
    ###
    def com_net_prox_node_report(self, node_name):
        """
        Gather various systems information about a node
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/report' % node_name)


    ###
    # Nodes/rrd
    ###


    ###
    # Nodes/rrddata
    ###


    ###
    # Nodes/spiceshell
    ###


    ###
    # Nodes/startall
    ###


    ###
    # Nodes/status
    ###


    ###
    # Nodes/stopall
    ###


    ###
    # Nodes/subscription
    ###


    ###
    # Nodes/syslog
    ###
    def com_net_prox_node_syslog(self, node_name):
        """
        Get a system log of node
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/syslog' % node_name)


    ###
    # Nodes/time
    ###
    def com_net_prox_node_time(self, node_name):
        """
        Get a system log of node
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/time' % node_name)


    ###
    # Nodes/version
    ###


    ###
    # Nodes/vncshell
    ###


    ###
    # Nodes/vncwebsocket
    ###


    ###
    # Nodes/vzdump
    ###


    ###
    # Pools
    ###
    def com_net_prox_pools(self):
        """
        Get the list of pools
        """
        return self.com_net_prox_api_call('get', 'pools')


    def com_net_prox_pool_create(self, post_data_json):
        """
        Create pool
        """
        return self.com_net_prox_api_call('post', 'pools', post_data_json)


    def com_net_prox_pool_update(self, pool_name, post_data_json):
        """
        Update pool
        """
        return self.com_net_prox_api_call('post', 'pools/%s' %s pool_name, post_data_json)


    def com_net_prox_pool_delete(self, pool_name):
        """
        Delete pool
        """
        return self.com_net_prox_api_call('delete', 'pools/%s' % pool_name)


    ###
    # Storage
    ###
    def com_net_prox_storage(self):
        """
        Get the list of storage
        """
        return self.com_net_prox_api_call('get', 'storage')


    def com_net_prox_storage_create(self, post_data_json):
        """
        Create a new storage.
        """
        return self.com_net_prox_api_call('post', 'storage', post_data_json)


    def com_net_prox_storage_config(self, storage_name):
        """
        Update storage configuration.
        """
        return self.com_net_prox_api_call('get', 'storage/%s' % storage_name)


    def com_net_prox_storage_config_update(self, storage_name, post_data_json):
        """
        Read storage configuration.
        """
        return self.com_net_prox_api_call('get', 'storage/%s' % storage_name, post_data_json)


    def com_net_prox_storage_config_delete(self, storage_name):
        """
        Delete storage configuration.
        """
        return self.com_net_prox_api_call('delete', 'storage/%s' % storage_name)


    ###
    # Version
    ###
    def com_net_prox_api_version(self):
        """
        # grab version of api from node
        """
        return self.com_net_prox_api_call('get', 'version')
