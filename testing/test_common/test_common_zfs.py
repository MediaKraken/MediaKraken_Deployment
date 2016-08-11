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
import pytest
import sys
sys.path.append("../common")
from MK_Common_ZFS import *


# check for ZFS compat
def test_MK_Common_ZFS_Available():
    MK_Common_ZFS_Available()


# get zpool list
def test_MK_Common_ZFS_Zpool_List():
    MK_Common_ZFS_Zpool_List()


# get zpool status
@pytest.mark.parametrize(("zpool"), [
    (None),
    ("spinning_rust"),
    ("spinning_rust_fake")])
def test_MK_Common_ZFS_Zpool_Status(zpool):
    MK_Common_ZFS_Zpool_Status(zpool)


# list snapshot
def test_MK_Common_ZFS_Snapshot_List():
    MK_Common_ZFS_Snapshot_List()


# list snapshot
@pytest.mark.parametrize(("zpool"), [
    (None),
    ("spinning_rust"),
    ("spinning_rust_fake")])
def test_MK_Common_ZFS_Snapshot_List(zpool):
    MK_Common_ZFS_Snapshot_List(zpool)


# delete snapshot
# def MK_Common_ZFS_Snapshot_Delete(snapshot):


# delete pool
@pytest.mark.parametrize(("zpool"), [
    (None),
    ("spinning_rust"),
    ("spinning_rust_fake")])
def test_MK_Common_ZFS_Zpool_Delete(zpool):
    MK_Common_ZFS_Zpool_Delete(zpool)


# scrub pool
@pytest.mark.parametrize(("zpool"), [
    (None),
    ("spinning_rust"),
    ("spinning_rust_fake")])
def test_MK_Common_ZFS_Zpool_Scrub(zpool):
    MK_Common_ZFS_Zpool_Scrub(zpool)


# replace drive in pool
# def MK_Common_ZFS_Zpool_Replace_Drive(zpool, target_drive, replacement_drive):


# create pool
# def MK_Common_ZFS_Zpool_Create(zpool, zpool_type, zpool_drives):


# pool stats

# set compression
# def MK_Common_ZFS_Zpool_Compression(zpool, zpool_compression, zpool_rate):


# get compression
@pytest.mark.parametrize(("zpool"), [
    (None),
    ("spinning_rust"),
    ("spinning_rust_fake")])
def test_MK_Common_ZFS_Zpool_Compression(zpool):
    MK_Common_ZFS_Zpool_Compression(zpool)


# set deduplication
# def MK_Common_ZFS_Zpool_Deduplication(zpool, zpool_dedup):


# send snapshot
# def MK_Common_ZFS_Zpool_Snapshot_Send(snapshot_begin, snapshot_end, receive_ip, port_no):


# receive snapshot
# def MK_Common_ZFS_Zpool_Snapshot_Receive(zpool_location, port_no):


# set cache drive
# def MK_Common_ZFS_Zpool_Cache_Drive(zpool):


# set larc2 drive
# def MK_Common_ZFS_Zpool_L2ARC(zpool):


# quota set for pool
# def MK_Common_ZFS_Zpool_Quota(zpool, quota_level):


# iostat, pool and interval
# def MK_Common_ZFS_Zpool_IOStat(zpool, interval):


# export zpool
# def MK_Common_ZFS_Zpool_Export(zpool):


# import pool
# def MK_Common_ZFS_Zpool_Import(zpool, zpool_new_name=None):


# rename zfs
# def MK_Common_ZFS_Rename(zpool, zpool_new_name):


# clone pool
# def MK_Common_ZFS_Clone(zpool_snap, zpool_clone):


# health check
def test_MK_Common_ZFS_Health_Check():
    MK_Common_ZFS_Health_Check()
