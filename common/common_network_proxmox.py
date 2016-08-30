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

'''

Node Methods

    getNodeServiceState(node,service)
"Read service properties"

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


OpenVZ Methods

    getContainerIndex(node,vmid)
"Directory index. Returns JSON"

    getContainerStatus(node,vmid)
"Get virtual machine status. Returns JSON"

    getContainerBeans(node,vmid)
"Get container user_beancounters. Returns JSON"

    getContainerConfig(node,vmid)
"Get container configuration. Returns JSON"

    getContainerInitLog(node,vmid)
"Read init log. Returns JSON"

    getContainerRRD(node,vmid)
"Read VM RRD statistics. Returns PNG"

    def getContainerRRDData(node,vmid)
"Read VM RRD statistics. Returns RRD"

KVM Methods

    getVirtualIndex(node,vmid)
"Directory index. Returns JSON"

    getVirtualStatus(node,vmid)
"Get virtual machine status. Returns JSON"

    getVirtualConfig(node,vmid)
"Get virtual machine configuration. Returns JSON"

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

    getNodeStorageRRD(node,storage)
"Read storage RRD statistics. Returns JSON"

    getNodeStorageRRDData(node,storage)
"Read storage RRD statistics. Returns JSON"


OpenVZ Methods

    createOpenvzContainer(node,post_data)
"Create or restore a container. Returns JSON Requires a dictionary of tuples formatted [('postname1','data'),('postname2','data')]"

    mountOpenvzPrivate(node,vmid)
"Mounts container private area. Returns JSON"

    shutdownOpenvzContainer(node,vmid)
"Shutdown the container. Returns JSON"

    startOpenvzContainer(node,vmid)
"Start the container. Returns JSON"

    stopOpenvzContainer(node,vmid)
"Stop the container. Returns JSON"

    unmountOpenvzPrivate(node,vmid)
"Unmounts container private area. Returns JSON"

    migrateOpenvzContainer(node,vmid,target)
"Migrate the container to another node. Creates a new migration task. Returns JSON"

KVM Methods

    createVirtualMachine(node,post_data)
"Create or restore a virtual machine. Returns JSON Requires a dictionary of tuples formatted [('postname1','data'),('postname2','data')]"

    cloneVirtualMachine(node,vmid,post_data)
"Create a copy of virtual machine/template. Returns JSON Requires a dictionary of tuples formatted [('postname1','data'),('postname2','data')]"

    resetVirtualMachine(node,vmid)
"Reset a virtual machine. Returns JSON"

    resumeVirtualMachine(node,vmid)
"Resume a virtual machine. Returns JSON"

    shutdownVirtualMachine(node,vmid)
"Shut down a virtual machine. Returns JSON"

    startVirtualMachine(node,vmid)
"Start a virtual machine. Returns JSON"

    stopVirtualMachine(node,vmid)
"Stop a virtual machine. Returns JSON"

    suspendVirtualMachine(node,vmid)
"Suspend a virtual machine. Returns JSON"

    migrateVirtualMachine(node,vmid,target)
"Migrate a virtual machine. Returns JSON"

    monitorVirtualMachine(node,vmid,command)
"Send monitor command to a virtual machine. Returns JSON"

    vncproxyVirtualMachine(node,vmid)
"Creates a VNC Proxy for a virtual machine. Returns JSON"

    rollbackVirtualMachine(node,vmid,snapname)
"Rollback a snapshot of a virtual machine. Returns JSON"

    getSnapshotConfigVirtualMachine(node,vmid,snapname)
"Get snapshot config of a virtual machine. Returns JSON"

DELETE Methods

OPENVZ

    deleteOpenvzContainer(node,vmid)
"Deletes the specified openvz container"

NODE

    deleteNodeNetworkConfig(node)
"Revert network configuration changes."

    deleteNodeInterface(node,interface)
"Delete network device configuration"

KVM

    deleteVirtualMachine(node,vmid)
"Destroy the vm (also delete all used/owned volumes)."

POOLS

    deletePool(poolid)
"Delete Pool"

STORAGE

    deleteStorageConfiguration(storageid)
"Delete storage configuration"

PUT Methods

NODE

    setNodeDNSDomain(node,domain)
"Set the nodes DNS search domain"

    setNodeSubscriptionKey(node,key)
"Set the nodes subscription key"

    setNodeTimeZone(node,timezone)
"Set the nodes timezone"

OPENVZ

    setOpenvzContainerOptions(node,vmid,post_data)
"Set openvz virtual machine options."

KVM

    setVirtualMachineOptions(node,vmide,post_data)
"Set KVM virtual machine options."

    sendKeyEventVirtualMachine(node,vmid, key)
"Send key event to virtual machine"

    unlinkVirtualMachineDiskImage(node,vmid, post_data)
"Unlink disk images"

POOLS

    setPoolData(poolid, post_data)
"Update pool data."

STORAGE

    updateStorageConfiguration(storageid,post_data)
"Update storage configuration"

'''
