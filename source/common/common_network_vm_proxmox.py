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

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class CommonNetworkProxMox(object):
    """
    Class for interfacing via proxmox
    """

    def __init__(self, node_addr, node_user, node_password):
        self.httpheaders = {'Accept': 'application/json',
                            'Content-Type': 'application/x-www-form-urlencoded'}
        self.full_url = ('https://%s:8006/api2/json/' % node_addr)
        self.node_user = node_user
        self.node_password = node_password

    # can't return a value with init.  So, broke out the connect to handle bad user/pass
    def com_net_prox_api_connect(self):
        self.api_response = requests.post(self.full_url + 'access/ticket', verify=False,
                                          data={'username': self.node_user,
                                                'password': self.node_password}).json()
        if self.api_response['data'] is None:
            return None
        self.prox_ticket = {'PVEAuthCookie': self.api_response['data']['ticket']}
        self.httpheaders['CSRFPreventionToken'] = str(
            self.api_response['data']['CSRFPreventionToken'])
        return self.api_response

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

    def com_net_prox_cluster_backup_create(self, post_data_json):
        """
        Create new vzdump backup job.
        """
        return self.com_net_prox_api_call('post', 'cluster/backup', post_data_json)

    def com_net_prox_cluster_backup_conf(self, backup_id):
        """
        Read vzdump backup job definition.
        """
        return self.com_net_prox_api_call('get', 'cluster/backup/%s' % backup_id)

    def com_net_prox_cluster_backup_update(self, backup_id, post_data_json):
        """
        Update vzdump backup job definition.
        """
        return self.com_net_prox_api_call('get', 'cluster/backup/%s' % backup_id, post_data_json)

    def com_net_prox_cluster_backup_delete(self, backup_id):
        """
        Delete vzdump backup job definition.
        """
        return self.com_net_prox_api_call('delete', 'cluster/backup/%s' % backup_id)

    ###
    # Cluster config
    ###
    def com_net_prox_cluster_config_nodes(self):
        return self.com_net_prox_api_call('get', 'cluster/config/nodes')

    # TODO node create
    # TODO node delete
    # TODO node info on cluster
    # TODO node join cluster
    # TODO node Get corosync totem protocol settings.

    ###
    # Cluster/firewall API
    ###
    def com_net_prox_cluster_firewall(self):
        """
        Directory index.
        """
        return self.com_net_prox_api_call('get', 'cluster/firewall')

    ###
    # Cluster/ha API
    ###
    def com_net_prox_cluster_ha(self):
        """
        Directory index.
        """
        return self.com_net_prox_api_call('get', 'cluster/ha')

    def com_net_prox_cluster_ha_groups(self):
        """
        Get HA groups.
        """
        return self.com_net_prox_api_call('get', 'cluster/ha/groups')

    def com_net_prox_cluster_ha_group_create(self, post_data_json):
        """
        Create a new HA group.
        """
        return self.com_net_prox_api_call('put', 'cluster/ha/groups', post_data_json)

    ###
    # Cluster/log API
    ###
    def com_net_prox_cluster_log(self):
        """
        Read cluster log
        """
        return self.com_net_prox_api_call('get', 'cluster/log')

    ###
    # Cluster/nextid API
    ###
    def com_net_prox_cluster_nextid(self):
        """
        Get next free VMID. If you pass an VMID it will raise an error if the ID is already used.
        """
        return self.com_net_prox_api_call('get', 'cluster/nextid')

    ###
    # Cluster/options API
    ###
    def com_net_prox_cluster_options(self):
        """
        Get datacenter options.
        """
        return self.com_net_prox_api_call('get', 'cluster/options')

    def com_net_prox_cluster_options_update(self, post_data_json):
        """
        Set datacenter options.
        """
        return self.com_net_prox_api_call('put', 'cluster/options', post_data_json)

    ###
    # Cluster/resources API
    ###
    def com_net_prox_cluster_resources(self):
        """
        Resources index (cluster wide).
        """
        return self.com_net_prox_api_call('get', 'cluster/resources')

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
    def com_net_prox_cluster_tasks(self):
        """
        List recent tasks (cluster wide).
        """
        return self.com_net_prox_api_call('get', 'cluster/tasks')

    ###
    # Nodes
    ###
    def com_net_prox_node_index(self, node_name):
        """
        Cluster node index.
        """
        return self.com_net_prox_api_call('get', node_name)

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

    def com_net_prox_node_lxc_create(self, node_name, host_name, memory_size,
                                     template_name, storage_id, os_type, cpu_limit, password):
        """
        create lxc on code
        """
        post_data = {'vmid': self.com_net_prox_cluster_nextid()['data'],
                     'ostemplate': template_name,
                     'hostname': host_name,
                     'storage': storage_id,
                     'cpulimit': cpu_limit,
                     'memory': memory_size,
                     'ostype': os_type,
                     'password': password,
                     # 'net': 'name=eth0',
                     # 'rootfs': '32',
                     # 'rootfs': 'vm-118-disk-1a, size=32G',
                     }
        print(('post %s' % post_data))
        return self.com_net_prox_api_call('post', 'nodes/%s/lxc' % node_name, post_data)

    def com_net_prox_node_lxc_status(self, node_name, vm_id):
        """
        Get a status of the lxc vm
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/lxc/%s/status/current'
                                          % (node_name, vm_id))

    def com_net_prox_node_lxc_start(self, node_name, vm_id):
        """
        Start lxc vm
        """
        return self.com_net_prox_api_call('post', 'nodes/%s/lxc/%s/status/start'
                                          % (node_name, vm_id))

    def com_net_prox_node_lxc_stop(self, node_name, vm_id):
        """
        Stop lxc vm
        """
        return self.com_net_prox_api_call('post', 'nodes/%s/lxc/%s/status/stop'
                                          % (node_name, vm_id))

    def com_net_prox_node_lxc_snaps(self, node_name, vm_id):
        """
        List snaps for lxc vm
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/lxc/%s/snapshot'
                                          % (node_name, vm_id))

    def com_net_prox_node_lxc_clone(self, node_name, vm_id, post_data_json):
        """
       Create clone for lxc vm
        """
        return self.com_net_prox_api_call('post', 'nodes/%s/lxc/%s/clone'
                                          % (node_name, vm_id), post_data_json)

    ###
    # Nodes/network
    ###
    def com_net_prox_net(self, node_name):
        """
        List available networks
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/network' % node_name)

    def com_net_prox_net_create(self, node_name, post_data_json):
        """
        List available networks
        """
        return self.com_net_prox_api_call('put', 'nodes/%s/network' % node_name, post_data_json)

    def com_net_prox_net_delete(self, node_name, post_data_json):
        """
        Revert network configuration changes.
        """
        return self.com_net_prox_api_call('delete', 'nodes/%s/network' % node_name, post_data_json)

    def com_net_prox_net_nic_conf(self, node_name, iface):
        """
        Read network device configuration
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/network/%s' % (node_name, iface))

    def com_net_prox_net_nic_conf_update(self, node_name, iface, post_data_json):
        """
        Update network device configuration
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/network/%s'
                                          % (node_name, iface), post_data_json)

    def com_net_prox_net_nic_conf_delete(self, node_name, iface):
        """
        Delete network device configuration
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/network/%s' % (node_name, iface))

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
        return self.com_net_prox_api_call('get', 'nodes/%s/qemu/%s/status/current'
                                          % (node_name, vm_id))

    def com_net_prox_node_qemu_start(self, node_name, vm_id):
        """
        Start qemu vm
        """
        return self.com_net_prox_api_call('post', 'nodes/%s/qemu/%s/status/start'
                                          % (node_name, vm_id))

    def com_net_prox_node_qemu_stop(self, node_name, vm_id):
        """
        Stop qemu vm
        """
        return self.com_net_prox_api_call('post', 'nodes/%s/qemu/%s/status/stop'
                                          % (node_name, vm_id))

    def com_net_prox_node_qemu_snaps(self, node_name, vm_id):
        """
        List snaps for qemu vm
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/qemu/%s/snapshot'
                                          % (node_name, vm_id))

    def com_net_prox_node_qemu_clone(self, node_name, vm_id, post_data_json):
        """
       Create clone for qemu vm
        """
        return self.com_net_prox_api_call('post', 'nodes/%s/qemu/%s/clone'
                                          % (node_name, vm_id), post_data_json)

    ###
    # Nodes/scan
    ###
    def com_net_prox_node_scan(self, node_name):
        """
        Index of available scan methods
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/scan' % node_name)

    def com_net_prox_node_scan_glusterfs(self, node_name, post_data_json):
        """
        Scan remote GlusterFS server.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/scan/glusterfs' % node_name,
                                          post_data_json)

    def com_net_prox_node_scan_iscsi(self, node_name, post_data_json):
        """
        Scan remote iSCSI server.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/scan/iscsi' % node_name,
                                          post_data_json)

    def com_net_prox_node_scan_lvm(self, node_name):
        """
        List local LVM volume groups.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/scan/lvm' % node_name)

    def com_net_prox_node_scan_lvmthin(self, node_name, post_data_json):
        """
        List local LVM Thin Pools.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/scan/lvmthin' % node_name,
                                          post_data_json)

    def com_net_prox_node_scan_nfs(self, node_name, post_data_json):
        """
        Scan remote NFS server.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/scan/nfs' % node_name,
                                          post_data_json)

    def com_net_prox_node_scan_usb(self, node_name):
        """
        List local USB devices.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/scan/usb' % node_name)

    def com_net_prox_node_scan_zfs(self, node_name):
        """
        Scan zfs pool list on local node.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/scan/zfs' % node_name)

    ###
    # Nodes/services
    ###
    def com_net_prox_node_services(self, node_name):
        """
        Service list.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/services' % node_name)

    def com_net_prox_node_services_ndx(self, node_name, service_id):
        """
        Directory index
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/services/%s' % (node_name, service_id))

    def com_net_prox_node_service_reload(self, node_name, service_id):
        """
        Reload service.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/services/%s/relaod'
                                          % (node_name, service_id))

    def com_net_prox_node_service_restart(self, node_name, service_id):
        """
        Restart service.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/services/%s/restart'
                                          % (node_name, service_id))

    def com_net_prox_node_service_start(self, node_name, service_id):
        """
        Start service.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/services/%s/start'
                                          % (node_name, service_id))

    def com_net_prox_node_service_state(self, node_name, service_id):
        """
        Service state.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/services/%s/state'
                                          % (node_name, service_id))

    def com_net_prox_node_service_stop(self, node_name, service_id):
        """
        Stop service.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/services/%s/stop'
                                          % (node_name, service_id))

    ###
    # Nodes/storage
    ###
    def com_net_prox_node_storage_status(self, node_name, post_data_json):
        """
        Get status for all datastores.
        """
        return self.com_net_prox_api_call('get', 'nodes/%s/storage' % node_name, post_data_json)

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
        return self.com_net_prox_api_call('post', 'pools/%s' % pool_name, post_data_json)

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


def com_net_prox_create_start_container(PROX_CONNECTION, JENKINS_BUILD_VIM, image_path):
    # build the container if doesn't already exist
    lxc_dict = {}
    for lxc_server in PROX_CONNECTION.com_net_prox_node_lxc_list('pve')['data']:
        lxc_dict[lxc_server['name']] = (lxc_server['vmid'], lxc_server['status'])
    print(('lxc: %s' % lxc_dict))
    if JENKINS_BUILD_VIM in lxc_dict:
        # container exists, make sure it's running
        print(('status: %s' % str(lxc_dict[JENKINS_BUILD_VIM][1])))
        # make sure it's started
        if lxc_dict[JENKINS_BUILD_VIM] != 'running':
            # start up the vm
            print(('start vim: %s' % lxc_dict[JENKINS_BUILD_VIM][0]))
            print((PROX_CONNECTION.com_net_prox_node_lxc_start(
                'pve', lxc_dict[JENKINS_BUILD_VIM][0])))
    else:
        # create the container
        print('create JENKINS_BUILD_VIM')
        print((PROX_CONNECTION.com_net_prox_node_lxc_create('pve', JENKINS_BUILD_VIM, 4096,
                                                            image_path,
                                                            'ZFS_VM', 'alpine', 8, 'metaman')))
        # keep an eye on task and see when its completed
        # while node.tasks(taskid).status()['status'] == 'running':
        #        time.sleep(1)

# this is for VM!!!  not container
#     # check status of vm
#     for vm_server in PROX_CONNECTION.com_net_prox_node_qemu_list('pve')['data']:
#         if vm_server['name'] == JENKINS_BUILD_VIM:
#             if vm_server['status'] == 'stopped':
#                 # start up the vm
#                 PROX_CONNECTION.com_net_prox_node_qemu_start('pve', vm_server['vmid'])
#                 time.sleep(60)  # wait for box to boot
#             break
