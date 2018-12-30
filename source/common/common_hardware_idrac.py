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

# https://github.com/MediaKraken-Dependancies/python-dracclient
import dracclient.client


class CommonHardwareIDrac(object):
    """
    Class for Dell IDrac
    """

    def __init__(self, ip_addr, user_name, user_password):
        self.idrac_inst = wsmanclient.client.DRACClient(ip_addr, user_name, user_password,
                                                        port=443, path='/wsman',
                                                        protocol='https')

    def com_hard_idrac_power_state(self):
        return self.idrac_inst.get_power_state()

    def com_hard_idrac_power_set(self, power_state=POWER_ON):
        """
        POWER_ON, POWER_OFF and REBOOT
        """
        return self.idrac_inst.set_power_state(power_state)

    def com_hard_idrac_boot_modes(self):
        return self.idrac_inst.list_boot_modes()

    def com_hard_idrac_list_boot(self):
        return self.idrac_inst.list_boot_devices()

    def com_hard_idrac_change_boot_order(self, boot_mode=boot_mode,
                                         boot_device_list=boot_device_list):
        '''
        Changes the boot device sequence for a boot mode.
        Required parameters:
            boot_mode: boot mode for which the boot device list is to be changed.
            boot_device_list: a list of boot device ids in an order representing
            the desired boot sequence.
        '''
        return self.idrac_inst.change_boot_device_order(boot_mode=boot_mode,
                                                        boot_device_list=boot_device_list)

    def com_hard_idrac_bios_list(self):
        return self.idrac_inst.list_bios_settings()

    def com_hard_idrac_bios_set(self, settings):
        '''
        settings: a dictionary containing the proposed values, with each key being
        the name of attribute and the value being the proposed value.
        '''
        return self.idrac_inst.set_bios_settings(settings=settings)

    def com_hard_idrac_bios_commit(self, reboot=False):
        '''
        reboot: indicates whether a RebootJob should also be created or not. Defaults to False.
        '''
        return self.idrac_inst.commit_pending_bios_changes(reboot)

    def com_hard_idrac_bios_abandon(self):
        return self.idrac_inst.abandon_pending_bios_changes()

    def com_hard_idrac_raid_list(self):
        return self.idrac_inst.list_raid_controllers()

    def com_hard_idrac_raid_list_vd(self):
        return self.idrac_inst.list_virtual_disks()

    def com_hard_idrac_raid_list_disks(self):
        return self.idrac_inst.list_physical_disks()


'''
# TODO
create_virtual_disk
Creates a virtual disk and returns a dictionary containing the commit_needed key with a boolean value indicating whether a config job must be created for the values to be applied.

Note The created virtual disk will be in pending state.
Required parameters:

raid_controller: id of the RAID controller.
physical_disks: ids of the physical disks.
raid_level: RAID level of the virtual disk.
size_mb: size of the virtual disk in megabytes.
Optional parameters:

disk_name: name of the virtual disk.
span_length: number of disks per span.
span_depth: number of spans in virtual disk.
delete_virtual_disk
Deletes a virtual disk and returns a dictionary containing the commit_needed key with a boolean value indicating whether a config job must be created for the values to be applied.

Note The deleted virtual disk will be in pending state. For the changes to be applied, a config job must be created and the node must be rebooted.
Required parameters:

virtual_disk: id of the virtual disk.
commit_pending_raid_changes
Applies all pending changes on a RAID controller by creating a config job and returns the id of the created job.

Required parameters:

raid_controller: id of the RAID controller.
Optional parameters:

reboot: indicates whether a RebootJob should also be created or not. Defaults to False.
abandon_pending_raid_changes
Deletes all pending changes on a RAID controller.

Note Once a config job has been submitted, it can no longer be abandoned.
Required parameters:

raid_controller: id of the RAID controller.
Inventory Management
list_cpus
Returns a list of installed CPUs.

list_memory
Returns a list of installed memory modules.

list_nics
Returns a list of NICs.

Job management
list_jobs
Returns a list of jobs from the job queue.

Optional parameters:

only_unfinished: indicates whether only unfinished jobs should be returned. Defaults to False.
get_job
Returns a job from the job queue.

Required parameters:

job_id: id of the job.
create_config_job
Creates a config job and returns the id of the created job.

Note In CIM (Common Information Model), weak association is used to name an instance of one class in the context of an instance of another class. SystemName and SystemCreationClassName are the attributes of the scoping system, while Name and CreationClassName are the attributes of the instance of the class, on which the CreateTargetedConfigJob method is invoked.
Required parameters:

resource_uri: URI of resource to invoke.
cim_creation_class_name: creation class name of the CIM object.
cim_name: name of the CIM object.
target: target device.
Optional parameters:

cim_system_creation_class_name: creation class name of the scoping system. Defaults to DCIM_ComputerSystem.
cim_system_name: name of the scoping system. Defaults to DCIM:ComputerSystem.
reboot: indicates whether a RebootJob should also be created or not. Defaults to False.
delete_pending_config
Cancels pending configuration.

Note Once a config job has been submitted, it can no longer be abandoned.
Note In CIM (Common Information Model), weak association is used to name an instance of one class in the context of an instance of another class. SystemName and SystemCreationClassName are the attributes of the scoping system, while Name and CreationClassName are the attributes of the instance of the class, on which the CreateTargetedConfigJob method is invoked.
Required parameters:

resource_uri: URI of resource to invoke.
cim_creation_class_name: creation class name of the CIM object.
cim_name: name of the CIM object.
target: target device.
Optional parameters:

cim_system_creation_class_name: creation class name of the scoping system. Defaults to DCIM_ComputerSystem.
cim_system_name: name of the scoping system. Defaults to DCIM:ComputerSystem.
reboot: indicates whether a RebootJob should also be created or not. Defaults to False.
Lifecycle controller management¶
get_lifecycle_controller_version
Returns the Lifecycle controller version as a tuple of integers.
'''
