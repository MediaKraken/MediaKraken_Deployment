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

import sys

sys.path.append('.')

# # check for ZFS compat
# def test_com_zfs_available():
#     """
#     Test function
#     """
#     common_zfs.com_zfs_available()
#
#
# # get zpool list
# def test_com_zfs_zpool_list():
#     """
#     Test function
#     """
#     common_zfs.com_zfs_zpool_list()
#
#
# # get zpool status
# @pytest.mark.parametrize(("zpool"), [
#     (None),
#     ("spinning_rust"),
#     ("spinning_rust_fake")])
# def test_com_zfs_zpool_status(zpool):
#     """
#     Test function
#     """
#     common_zfs.com_zfs_zpool_status(zpool)
#
#
# # list snapshot
# def test_com_zfs_snapshot_list():
#     """
#     Test function
#     """
#     common_zfs.com_zfs_snapshot_list()
#
#
# # list snapshot
# @pytest.mark.parametrize(("zpool"), [
#     (None),
#     ("spinning_rust"),
#     ("spinning_rust_fake")])
# def test_com_zfs_snapshot_list(zpool):
#     """
#     Test function
#     """
#     common_zfs.com_zfs_snapshot_list(zpool)
#
#
# # delete snapshot
# # def common_zfs.com_zfs_Snapshot_Delete(snapshot):
#
#
# # delete pool
# @pytest.mark.parametrize(("zpool"), [
#     (None),
#     ("spinning_rust"),
#     ("spinning_rust_fake")])
# def test_com_zfs_zpool_delete(zpool):
#     """
#     Test function
#     """
#     common_zfs.com_zfs_zpool_delete(zpool)
#
#
# # scrub pool
# @pytest.mark.parametrize(("zpool"), [
#     (None),
#     ("spinning_rust"),
#     ("spinning_rust_fake")])
# def test_com_zfs_zpool_scrub(zpool):
#     """
#     Test function
#     """
#     common_zfs.com_zfs_zpool_scrub(zpool)
#
#
# # replace drive in pool
# # def common_zfs.com_zfs_Zpool_Replace_Drive(zpool, target_drive, replacement_drive):
#
#
# # create pool
# # def common_zfs.com_zfs_Zpool_Create(zpool, zpool_type, zpool_drives):
#
#
# # pool stats
#
# # set compression
# # def common_zfs.com_zfs_Zpool_Compression(zpool, zpool_compression, zpool_rate):
#
#
# # get compression
# @pytest.mark.parametrize(("zpool"), [
#     (None),
#     ("spinning_rust"),
#     ("spinning_rust_fake")])
# def test_com_zfs_zpool_compression(zpool):
#     """
#     Test function
#     """
#     common_zfs.com_zfs_zpool_compression(zpool)
#
#
# # set deduplication
# # def common_zfs.com_zfs_Zpool_Deduplication(zpool, zpool_dedup):
#
#
# # send snapshot
# # def common_zfs.com_zfs_Zpool_Snapshot_Send(snapshot_begin, snapshot_end, receive_ip, port_no):
#
#
# # receive snapshot
# # def common_zfs.com_zfs_Zpool_Snapshot_Receive(zpool_location, port_no):
#
#
# # set cache drive
# # def common_zfs.com_zfs_Zpool_Cache_Drive(zpool):
#
#
# # set larc2 drive
# # def common_zfs.com_zfs_Zpool_L2ARC(zpool):
#
#
# # quota set for pool
# # def common_zfs.com_zfs_Zpool_Quota(zpool, quota_level):
#
#
# # iostat, pool and interval
# # def common_zfs.com_zfs_Zpool_IOStat(zpool, interval):
#
#
# # export zpool
# # def common_zfs.com_zfs_Zpool_Export(zpool):
#
#
# # import pool
# # def common_zfs.com_zfs_Zpool_Import(zpool, zpool_new_name=None):
#
#
# # rename zfs
# # def common_zfs.com_zfs_Rename(zpool, zpool_new_name):
#
#
# # clone pool
# # def common_zfs.com_zfs_Clone(zpool_snap, zpool_clone):
#
#
# # health check
# def test_com_zfs_health_check():
#     """
#     Test function
#     """
#     common_zfs.com_zfs_health_check()
