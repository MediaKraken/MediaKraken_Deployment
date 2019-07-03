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

import platform
import subprocess


def com_zfs_available():
    """
    Check for ZFS compat
    """
    if platform.system() == "Linux" or platform.system() == "FreeBSD":
        try:
            subprocess.check_call(["zfs", "-h"])
        except:
            return False
        return True
    else:
        return False


def com_zfs_zpool_list():
    """
    Get zpool list
    """
    proc = subprocess.Popen(['zpool', 'list'], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_zpool_status(zpool=None):
    """
    Get zpool status
    """
    if zpool is not None:
        proc = subprocess.Popen(
            ['zpool', 'status', zpool], stdout=subprocess.PIPE, shell=False)
    else:
        proc = subprocess.Popen(['zpool', 'status'], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_snapshot_list(zpool=None):
    """
    List snapshot
    """
    if zpool is not None:
        proc = subprocess.Popen(['zfs', 'list', '-H', '-t', 'snapshot', zpool],
                                stdout=subprocess.PIPE, shell=False)
    else:
        proc = subprocess.Popen(
            ['zfs', 'list', '-H', '-t', 'snapshot'], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_snapshot_delete(snapshot):
    """
    Delete snapshot
    """
    proc = subprocess.Popen(
        ['zfs', 'destroy', snapshot], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_zpool_delete(zpool):
    """
    Delete pool
    """
    proc = subprocess.Popen(
        ['zpool', 'destroy', zpool], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_zpool_scrub(zpool=None):
    """
    Scrub pool
    """
    if zpool is not None:
        proc = subprocess.Popen(
            ['zpool', 'scrub', zpool], stdout=subprocess.PIPE, shell=False)
    else:
        proc = subprocess.Popen(['zpool', 'scrub'], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_zpool_replace_drive(zpool, target_drive, replacement_drive):
    """
    Replace drive in pool
    """
    proc = subprocess.Popen(['zpool', 'replace', zpool, target_drive, replacement_drive],
                            stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_zpool_create(zpool, zpool_type, zpool_drives):
    """
    Create pool
    """
    proc = subprocess.Popen(['zpool', 'create', zpool, zpool_type, zpool_drives],
                            stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


# pool stats

def com_zfs_zpool_compression(zpool, zpool_compression, zpool_rate):
    """
    Set compression
    """
    proc = subprocess.Popen(
        ['zfs', 'set', 'compression=on', zpool], stdout=subprocess.PIPE, shell=False)
    proc = subprocess.Popen(['zfs', 'set', 'compression=gzip-' + zpool_compression, zpool],
                            stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_zpool_compression_ratio(zpool):
    """
    Get compression ratio
    """
    proc = subprocess.Popen(
        ['zfs', 'get', 'compressratio', zpool], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_zpool_deduplication(zpool, zpool_dedup):
    """
    Set deduplication
    """
    if zpool_dedup:
        proc = subprocess.Popen(
            ['zfs', 'set', 'dedup=on', zpool], stdout=subprocess.PIPE, shell=False)
    else:
        proc = subprocess.Popen(
            ['zfs', 'set', 'dedup=off', zpool], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_zpool_snapshot_send(snapshot_begin, snapshot_end, receive_ip, port_no):
    """
    Send snapshot
    """
    proc = subprocess.Popen(['zfs send -R -i storage_pool@-2015-11-11 storage_pool@-2015-11-21'
                             ' | mbuffer -s 128k -m 1G -O 10.1.0.7:9191'], stdout=subprocess.PIPE,
                            shell=False)
    return proc.stdout.read()


def com_zfs_zpool_snapshot_receive(zpool_location, port_no):
    """
    Receive snapshot
    """
    proc = subprocess.Popen(['mbuffer', '-s', '128k', '-m', '1G', '-I', port_no, '|', 'zfs',
                             'receive', '-Fudv', zpool_location], stdout=subprocess.PIPE,
                            shell=False)
    return proc.stdout.read()


def com_zfs_zpool_cache_drive(zpool):
    """
    Set cache drive
    """
    return proc.stdout.read()


def com_zfs_zpool_l2arc(zpool):
    """
    Set larc2 drive
    """
    return proc.stdout.read()


def com_zfs_zpool_quota(zpool, quota_level):
    """
    Quota set for pool
    """
    # TODO by user and groups?
    # zfs create students/compsci
    # zfs set userquota@student1=10G students/compsci
    proc = subprocess.Popen(
        ['zfs', 'set', 'quota=' + quota_level, zpool], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_zpool_iostat(zpool, interval):
    """
    iostat, pool and interval
    """
    proc = subprocess.Popen(
        ['zpool', 'iostat', zpool, interval], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_zpool_export(zpool):
    """
    Export zpool
    """
    proc = subprocess.Popen(['zpool', 'export', zpool], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_zpool_import(zpool, zpool_new_name=None):
    """
    Import pool
    """
    if zpool_new_name is not None:
        proc = subprocess.Popen(
            ['zpool', 'import', zpool, zpool_new_name], stdout=subprocess.PIPE, shell=False)
    else:
        proc = subprocess.Popen(
            ['zpool', 'import', zpool], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_rename(zpool, zpool_new_name):
    """
    Rename zfs
    """
    proc = subprocess.Popen(
        ['zfs', 'rename', zpool, zpool_new_name], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_clone(zpool_snap, zpool_clone):
    """
    Clone pool
    """
    proc = subprocess.Popen(
        ['zfs', 'clone', zpool_snap, zpool_clone], stdout=subprocess.PIPE, shell=False)
    return proc.stdout.read()


def com_zfs_health_check():
    """
    Health check
    """
    try:
        proc = subprocess.Popen(
            ['zpool', 'list', '-H', '-o', 'health'], stdout=subprocess.PIPE, shell=False)
        return proc.stdout.read()
    except OSError as err_code:  # typically program doesn't exist
        return None
