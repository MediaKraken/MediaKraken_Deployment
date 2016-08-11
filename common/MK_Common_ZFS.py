'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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
import platform
import logging


# check for ZFS compat
def MK_Common_ZFS_Available():
    if platform.system() == "Linux" or platform.system() == "FreeBSD":
        try:        
            subprocess.check_call(["zfs", "-h"])
        except:
            return False
        return True
    else:
        return False


# get zpool list
def MK_Common_ZFS_Zpool_List():
    proc = subprocess.Popen(['zpool', 'list'], stdout=subprocess.PIPE)
    return proc.stdout.read()


# get zpool status
def MK_Common_ZFS_Zpool_Status(zpool=None):
    if zpool is not None:
        proc = subprocess.Popen(['zpool', 'status', zpool], stdout=subprocess.PIPE)
    else:
        proc = subprocess.Popen(['zpool', 'status'], stdout=subprocess.PIPE)
    return proc.stdout.read()


# list snapshot
def MK_Common_ZFS_Snapshot_List(zpool=None):
    if zpool is not None:
        proc = subprocess.Popen(['zfs', 'list', '-H', '-t', 'snapshot', zpool], stdout=subprocess.PIPE)
    else:
        proc = subprocess.Popen(['zfs', 'list', '-H', '-t', 'snapshot'], stdout=subprocess.PIPE)
    return proc.stdout.read()


# delete snapshot
def MK_Common_ZFS_Snapshot_Delete(snapshot):
    proc = subprocess.Popen(['zfs', 'destroy', snapshot], stdout=subprocess.PIPE)
    return proc.stdout.read()


# delete pool
def MK_Common_ZFS_Zpool_Delete(zpool):
    proc = subprocess.Popen(['zpool', 'destroy', zpool], stdout=subprocess.PIPE)
    return proc.stdout.read()


# scrub pool
def MK_Common_ZFS_Zpool_Scrub(zpool=None):
    if zpool is not None:
        proc = subprocess.Popen(['zpool', 'scrub', zpool], stdout=subprocess.PIPE)
    else:
        proc = subprocess.Popen(['zpool', 'scrub'], stdout=subprocess.PIPE)
    return proc.stdout.read()


# replace drive in pool
def MK_Common_ZFS_Zpool_Replace_Drive(zpool, target_drive, replacement_drive):
    proc = subprocess.Popen(['zpool', 'replace', zpool, target_drive, replacement_drive], stdout=subprocess.PIPE)
    return proc.stdout.read()


# create pool
def MK_Common_ZFS_Zpool_Create(zpool, zpool_type, zpool_drives):
    proc = subprocess.Popen(['zpool', 'create', zpool, zpool_type, zpool_drives], stdout=subprocess.PIPE)
    return proc.stdout.read()


# pool stats

# set compression
def MK_Common_ZFS_Zpool_Compression(zpool, zpool_compression, zpool_rate):
    proc = subprocess.Popen(['zfs', 'set', 'compression=on', zpool], stdout=subprocess.PIPE)
    proc = subprocess.Popen(['zfs', 'set', 'compression=gzip-' + zpool_compression, zpool], stdout=subprocess.PIPE)
    return proc.stdout.read()


# get compression
def MK_Common_ZFS_Zpool_Compression(zpool):
    proc = subprocess.Popen(['zfs', 'get', 'compressratio', zpool], stdout=subprocess.PIPE)
    return proc.stdout.read()


# set deduplication
def MK_Common_ZFS_Zpool_Deduplication(zpool, zpool_dedup):
    if zpool_dedup:
        proc = subprocess.Popen(['zfs', 'set', 'dedup=on', zpool], stdout=subprocess.PIPE)
    else:
        proc = subprocess.Popen(['zfs', 'set', 'dedup=off', zpool], stdout=subprocess.PIPE)
    return proc.stdout.read()


# send snapshot
def MK_Common_ZFS_Zpool_Snapshot_Send(snapshot_begin, snapshot_end, receive_ip, port_no):
    proc = subprocess.Popen(['zfs send -R -i storage_pool@-2015-11-11 storage_pool@-2015-11-21  | mbuffer -s 128k -m 1G -O 10.1.0.7:9191'], stdout=subprocess.PIPE)
    return proc.stdout.read()


# receive snapshot
def MK_Common_ZFS_Zpool_Snapshot_Receive(zpool_location, port_no):
    proc = subprocess.Popen(['mbuffer', '-s', '128k', '-m', '1G', '-I', port_no, '|', 'zfs', 'receive', '-Fudv', zpool_location], stdout=subprocess.PIPE)
    return proc.stdout.read()


# set cache drive
def MK_Common_ZFS_Zpool_Cache_Drive(zpool):
    return proc.stdout.read()


# set larc2 drive
def MK_Common_ZFS_Zpool_L2ARC(zpool):
    return proc.stdout.read()


# quota set for pool
def MK_Common_ZFS_Zpool_Quota(zpool, quota_level):
# TODO by user and groups?
# zfs create students/compsci
# zfs set userquota@student1=10G students/compsci
    proc = subprocess.Popen(['zfs', 'set', 'quota=' + quota_level, zpool], stdout=subprocess.PIPE)
    return proc.stdout.read()


# iostat, pool and interval
def MK_Common_ZFS_Zpool_IOStat(zpool, interval):
    proc = subprocess.Popen(['zpool', 'iostat', zpool, interval], stdout=subprocess.PIPE)
    return proc.stdout.read()


# export zpool
def MK_Common_ZFS_Zpool_Export(zpool):
    proc = subprocess.Popen(['zpool', 'export', zpool], stdout=subprocess.PIPE)
    return proc.stdout.read()


# import pool
def MK_Common_ZFS_Zpool_Import(zpool, zpool_new_name=None):
    if zpool_new_name is not None:
        proc = subprocess.Popen(['zpool', 'import', zpool, zpool_new_name], stdout=subprocess.PIPE)
    else:
        proc = subprocess.Popen(['zpool', 'import', zpool], stdout=subprocess.PIPE)
    return proc.stdout.read()


# rename zfs
def MK_Common_ZFS_Rename(zpool, zpool_new_name):
    proc = subprocess.Popen(['zfs', 'rename', zpool, zpool_new_name], stdout=subprocess.PIPE)
    return proc.stdout.read()


# clone pool
def MK_Common_ZFS_Clone(zpool_snap, zpool_clone):
    proc = subprocess.Popen(['zfs', 'clone', zpool_snap, zpool_clone], stdout=subprocess.PIPE)
    return proc.stdout.read()


# health check
def MK_Common_ZFS_Health_Check():
    proc = subprocess.Popen(['zpool', 'list', '-H', '-o', 'health'], stdout=subprocess.PIPE)
    return proc.stdout.read()
