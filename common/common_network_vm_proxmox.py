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
    # Cluster API
    ###
    def com_net_prox_api_version(self):
        """
        # grab version of api from node
        """
        return self.com_net_prox_api_call('get', 'version')


    def com_net_prox_cluster_ndx(self):
        """
        Get the index of the cluster
        """
        return self.com_net_prox_api_call('get', 'cluster')


    ###
    # LXC api calls
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


    ###
    # QEMU api calls
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
