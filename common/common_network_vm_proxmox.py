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
from pyproxmox import *


class CommonNetworkProxMox(object):
    """
    Class for interfacing via proxmox
    """
    def __init__(self, node_addr, node_user, node_password):
        self.proxmox_instance = pyproxmox(prox_auth(node_addr, node_user, node_password))


    def com_net_prox_status(self):
        return self.proxmox_instance.getClusterStatus()


    def com_net_prox_backup_sch(self):
        return self.proxmox_instance.getClusterBackupSchedule()


    def com_net_prox_cluster_nextid(self):
        return self.proxmox_instance.getClusterVmNextId()


    def com_net_prox_net_list(self, node_name='pve'):
        return self.proxmox_instance.getNodeNetworks(node_name)


    def com_net_prox_net_interface(self, node_name='pve', node_interface='eth0'):
        return self.proxmox_instance.getNodeInterface(node_name, node_interface)


    def com_net_prox_service_list(self, node_name='pve'):
        return self.proxmox_instance.getNodeServiceList(node_name)


    def com_net_prox_openvz_containers(self, node_name='pve'):
        return self.proxmox_instance.getNodeContainerIndex(node_name)


    def com_net_prox_vm_containers(self, node_name='pve'):
        return self.proxmox_instance.getNodeVirtualIndex(node_name)


    def com_net_prox_storage_status(self, node_name='pve'):
        return self.proxmox_instance.getNodeStorage(node_name)


    def com_net_prox_node_status(self, node_name='pve'):
        return self.proxmox_instance.getNodeStatus(node_name)


    def com_net_prox_node_system_logs(self, node_name='pve'):
        return self.proxmox_instance.getNodeSyslog(node_name)


    def com_net_prox_net_dns(self, node_name='pve'):
        return self.proxmox_instance.getNodeDNS(node_name)


    def com_net_prox_finished_tasks(self, node_name='pve'):
        return self.proxmox_instance.getNodeFinishedTasks(node_name)


    def com_net_prox_get_usb(self, node_name='pve'):
        return self.proxmox_instance.getNodeUSB(node_name)


    def com_net_prox_lvm_group(self, node_name='pve'):
        return self.proxmox_instance.getNodeLVMGroups(node_name)


    def com_net_prox_nfs(self, node_name='pve'):
        return self.proxmox_instance.getRemoteNFS(node_name)


    def com_net_prox_iscsi(self, node_name='pve'):
        return self.proxmox_instance.getRemoteiSCSI(node_name)


    def com_net_prox_scan_methods(self, node_name='pve'):
        return self.proxmox_instance.getNodeScanMethods(node_name)


    def com_net_prox_service_props(self, node_name='pve', service):
        return self.proxmox_instance.getNodeServiceState(node_name, service)

'''
    getNodeRRD(node)
"Read node RRD statistics. Returns PNG"

    getNodeRRDData(node)
"Read node RRD statistics. Returns RRD"

    getNodeBeans(node)
"Get user_beancounters failcnt for all active containers. Returns JSON"

    getNodeTaskByUPID(node,upid)
"Get tasks by UPID. Returns JSON"

    getNodeTaskLogByUPID(node,upid)
"Read task log. Returns JSON"

    getNodeTaskStatusByUPID(node,upid)
"Read task status. Returns JSON"

'''
    def com_net_prox_lxc_index(self, node_name='pve', vm_id):
        return self.proxmox_instance.getContainerIndex(node_name, vm_id)


    def com_net_prox_lxc_status(self, node_name='pve', vm_id):
        return self.proxmox_instance.getContainerStatus(node_name, vm_id)


    def com_net_prox_lxc_config(self, node_name='pve', vm_id):
        return self.proxmox_instance.getContainerConfig(node_name, vm_id)


    def com_net_prox_lxc_init_log(self, node_name='pve', vm_id):
        return self.proxmox_instance.getContainerInitLog(node_name, vm_id)

'''


    getContainerBeans(node,vmid)
"Get container user_beancounters. Returns JSON"

    getContainerRRD(node,vmid)
"Read VM RRD statistics. Returns PNG"

    def getContainerRRDData(node,vmid)
"Read VM RRD statistics. Returns RRD"

'''
    def com_net_prox_kvm_index(self, node_name='pve', vm_id):
        return self.proxmox_instance.getVirtualIndex(node_name, vm_id)


    def com_net_prox_kvm_status(self, node_name='pve', vm_id):
        return self.proxmox_instance.getVirtualStatus(node_name, vm_id)


    def com_net_prox_kvm_config(self, node_name='pve', vm_id):
        return self.proxmox_instance.getVirtualConfig(node_name, vm_id)

'''

    getVirtualRRD(node,vmid)
"Read VM RRD statistics. Returns JSON"

    getVirtualRRDData(node,vmid)
"Read VM RRD statistics. Returns JSON"

Storage Methods

    getStorageVolumeData(node,storage,volume)
"Get volume attributes. Returns JSON"

    getStorageConfig(storage)
"Read storage config. Returns JSON"

    getNodeStorageContent(node,storage)
"List storage content. Returns JSON"
'''

    def com_net_prox_lxc_start(self, node_name='pve', vm_id):
        return self.proxmox_instance.startOpenvzContainer(node_name, vm_id)

'''
    getNodeStorageRRD(node,storage)
"Read storage RRD statistics. Returns JSON"

    getNodeStorageRRDData(node,storage)
"Read storage RRD statistics. Returns JSON"

'''
    def com_net_prox_lxc_create(self, node_name='pve', vm_id):
        return self.proxmox_instance.createOpenvzContainer(node_name, vm_id)


    def com_net_prox_lxc_mnt_private(self, node_name='pve', vm_id):
        return self.proxmox_instance.mountOpenvzPrivate(node_name, vm_id)


    def com_net_prox_lxc_umnt_private(self, node_name='pve', vm_id):
        return self.proxmox_instance.unmountOpenvzPrivate(node_name, vm_id)


    def com_net_prox_lxc_start(self, node_name='pve', vm_id):
        return self.proxmox_instance.startOpenvzContainer(node_name, vm_id)


    def com_net_prox_lxc_stop(self, node_name='pve', vm_id):
        return self.proxmox_instance.stopOpenvzContainer(node_name, vm_id)


    def com_net_prox_lxc_shutdown(self, node_name='pve', vm_id):
        return self.proxmox_instance.shutdownOpenvzContainer(node_name, vm_id)


    def com_net_prox_lxc_migreate(self, node_name='pve', vm_id, target_node):
        return self.proxmox_instance.migrateOpenvzContainer(node_name, vm_id, target_node)


    def com_net_prox_kvm_create(self, node_name='pve', vm_id, vm_config):
        return self.proxmox_instance.createVirtualMachine(node_name, vm_id, vm_config)


    def com_net_prox_kvm_clone(self, node_name='pve', vm_id, vm_config):
        return self.proxmox_instance.cloneVirtualMachine(node_name, vm_id, vm_config)


    def com_net_prox_kvm_reset(self, node_name='pve', vm_id):
        return self.proxmox_instance.resetVirtualMachine(node_name, vm_id)


    def com_net_prox_kvm_resume(self, node_name='pve', vm_id):
        return self.proxmox_instance.resumeVirtualMachine(node_name, vm_id)


    def com_net_prox_kvm_shutdown(self, node_name='pve', vm_id):
        return self.proxmox_instance.shutdownVirtualMachine(node_name, vm_id)


    def com_net_prox_kvm_start(self, node_name='pve', vm_id):
        return self.proxmox_instance.startVirtualMachine(node_name, vm_id)


    def com_net_prox_kvm_stop(self, node_name='pve', vm_id):
        return self.proxmox_instance.stopVirtualMachine(node_name, vm_id)


    def com_net_prox_kvm_suspend(self, node_name='pve', vm_id):
        return self.proxmox_instance.suspendVirtualMachine(node_name, vm_id)


    def com_net_prox_kvm_migrate(self, node_name='pve', vm_id, target_node):
        return self.proxmox_instance.migrateVirtualMachine(node_name, vm_id, target_node)


    def com_net_prox_kvm_monitor_cmd(self, node_name='pve', vm_id, monitor_command):
        return self.proxmox_instance.monitorVirtualMachine(node_name, vm_id, monitor_command)


    def com_net_prox_kvm_vnc_proxy(self, node_name='pve', vm_id):
        return self.proxmox_instance.vncproxyVirtualMachine(node_name, vm_id)


    def com_net_prox_kvm_snap_rollback(self, node_name='pve', vm_id, snap_name):
        return self.proxmox_instance.rollbackVirtualMachine(node_name, vm_id, snap_name)


    def com_net_prox_kvm_snap_config(self, node_name='pve', vm_id, snap_name):
        return self.proxmox_instance.getSnapshotConfigVirtualMachine(node_name, vm_id, snap_name)


    def com_net_prox_lxc_delete(self, node_name='pve', vm_id):
        return self.proxmox_instance.deleteOpenvzContainer(node_name, vm_id)
'''

NODE

    deleteNodeNetworkConfig(node)
"Revert network configuration changes."

'''

    def com_net_prox_nic_delete(self, node_name='pve', vm_id, nic_name):
        return self.proxmox_instance.deleteNodeInterface(node_name, vm_id, nic_name)


    def com_net_prox_kvm_delete(self, node_name='pve', vm_id):
        return self.proxmox_instance.deleteVirtualMachine(node_name, vm_id)

'''


POOLS

    deletePool(poolid)
"Delete Pool"

STORAGE

    deleteStorageConfiguration(storageid)
"Delete storage configuration"

'''
    def com_net_prox_set_dns(self, node_name='pve', dns_domain):
        return self.proxmox_instance.setNodeDNSDomain(node_name, dns_domain)


    def com_net_prox_set_subscription(self, node_name='pve', sub_key):
        return self.proxmox_instance.setNodeSubscriptionKey(node_name, sub_key)


    def com_net_prox_set_timezone(self, node_name='pve', timezone):
        return self.proxmox_instance.setNodeTimeZone(node_name, timezone)


    def com_net_prox_lxc_set_config(self, node_name='pve', vm_id, vm_options):
        return self.proxmox_instance.setOpenvzContainerOptions(node_name, vm_id, vm_options)
'''

KVM

'''
    def com_net_prox_kvm_set_config(self, node_name='pve', vm_id, vm_options):
        return self.proxmox_instance.setVirtualMachineOptions(node_name, vm_id, vm_options)
'''

    sendKeyEventVirtualMachine(node,vmid, key)
"Send key event to virtual machine"

    unlinkVirtualMachineDiskImage(node,vmid, post_data)
"Unlink disk images"

POOLS

    setPoolData(poolid, post_data)
"Update pool data."

'''

    def com_net_prox_storage_config(self, storage_id, storage_options):
        return self.proxmox_instance.updateStorageConfiguration(storage_id, storage_options)


stuff = CommonNetworkProxMox('10.0.0.190', 'root@pam', 'jenkinsbuild')
print(stuff.com_net_prox_status())
print(stuff.com_net_prox_backup_sch())
print(stuff.com_net_prox_cluster_nextid())
print(stuff.com_net_prox_net_list())
print(stuff.com_net_prox_net_interface())
print(stuff.com_net_prox_service_list())
print(stuff.com_net_prox_openvz_containers())
print(stuff.com_net_prox_vm_containers())
print(stuff.com_net_prox_storage_status())
print(stuff.com_net_prox_node_status())
print(stuff.com_net_prox_node_system_logs())
print(stuff.com_net_prox_net_dns())
print(stuff.com_net_prox_finished_tasks())
print(stuff.com_net_prox_get_usb())
print(stuff.com_net_prox_lvm_group())
print(stuff.com_net_prox_nfs())
print(stuff.com_net_prox_iscsi())
print(stuff.com_net_prox_scan_methods())
