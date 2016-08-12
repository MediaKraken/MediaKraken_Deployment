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
from common_cloud import *


# get list of all backups
def Test_common_cloud_Backup_List():
    common_cloud_Backup_List()


# store file in cloud
# def common_cloud_File_Store(cloud_type, file_path_name, file_save_name, backup_bucket=False):


# delete file in cloud
# def common_cloud_File_Delete(cloud_type, file_name, backup_bucket=False):


# list files in cloud
# def common_cloud_File_List(cloud_type, file_path=None, backup_bucket=False):


# fetch file from cloud
# def common_cloud_File_Retrieve(cloud_type, file_name, file_location):


# rename file on cloud
# def common_cloud_File_Rename(cloud_type, file_from, file_to):


# create direcgtory in cloud
@pytest.mark.parametrize(("cloud_type", "dir_name"), [
    ("awss3", "dir_test"),
    ("awss3", "dir_test"), # dupe test
    ("dropbox", "dir_test"),
    ("dropbox", "dir_test"), # dupe test
    ("google", "dir_test"),
    ("google", "dir_test"), # dupe test
    ("local", "dir_test"),
    ("local", "dir_test"), # dupe test
    ("onedrive", "dir_test"),
    ("onedrive", "dir_test")]) # dupe test
def Test_common_cloud_Create_Folder(self, cloud_type, dir_name):
    common_cloud_Create_Folder(cloud_type, dir_name)
