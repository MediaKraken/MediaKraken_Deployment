"""
  Copyright (C) 2020 Quinn D Granfor <spootdev@gmail.com>

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
"""

import asyncio
import sys

from common import common_network_ssh
from common import common_system


# to run on the proxmox server
# apt install parted

async def main(loop):
    # connection to proxmox instance
    prox_inst = common_network_ssh.CommonNetworkSSH(host='10.0.0.200',
                                                    user_name='root',
                                                    user_password='ackack100')
    # grab the disk list
    # disk_out = prox_inst.com_net_ssh_run_command("find /dev/disk/by-id/ -type l"
    #                                              "|xargs -I{} ls -l {}"
    #                                              "|grep -v -E '[0-9]$' |sort -k11"
    #                                              "|cut -d' ' -f9,10,11")
    # disk list
    disk_out = prox_inst.com_net_ssh_run_command("blkid")
    for disk in disk_out.split(b'\r\n'):
        disk = disk.decode('utf-8')
        #print(disk, flush=True)
        disk_type = None
        '''/dev/sdaf1: LABEL="tank6" UUID="9999926442887589461" UUID_SUB="4572218617240751467"
         TYPE="zfs_member" PARTUUID="32f0258c-a0e3-4e70-a3b6-2fe936dbbc27"'''
        try:  # go for six
            disk_name, disk_label, disk_uuid, \
            disk_sub_uuid, disk_type, disk_part_uuid = disk.split(' ')
        except:  # go for four
            try:
                """/dev/sda2: UUID="29DD-66E1" TYPE="vfat"
                 PARTUUID="e82a7738-6216-4675-b54c-6740c3ebb42c"""
                disk_name, disk_uuid, disk_type, disk_part_uuid = disk.split(' ')
            except:
                try:
                    """b'/dev/mapper/pve-swap:
                     UUID="961ca3fe-1f6b-4638-9c47-f865d0b94143" TYPE="swap"'"""
                    disk_name, disk_uuid, disk_type = disk.split(' ')
                except:
                    """b'/dev/sda1: PARTUUID="cea3775f-d906-4ad7-aee4-4ae1644bacc0"'"""
                    pass
        print(disk_type)
        if disk_type is not None and disk_type.find('TYPE="zfs_member"') != -1:
            # can get partition number from the last digit of disk_name
            prox_inst.com_net_ssh_run_command("parted -s %s rm %s" %
                                              (disk_name.replace(':', '',)[:-1],
                                               disk_name.replace(':', '',)[-1:]))
            prox_inst.com_net_ssh_run_command("parted -s -a optimal %s "
                                              "mklabel gpt -- mkpart primary xfs 1 -1"
                                              % disk_name.replace(':', ''))
            prox_inst.com_net_ssh_run_command("mkfs.xfs -f %s1" % disk_name.replace(':', ''))

    # release ssh connection
    prox_inst.com_net_ssh_close()


if __name__ == "__main__":
    # verify this program isn't already running!
    if common_system.com_process_list(
            process_name='/usr/bin/python3 /mediakraken/async_minio_buildout.py'):
        sys.exit(0)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
