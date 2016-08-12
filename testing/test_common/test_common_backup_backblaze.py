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
import os
import pytest
import sys
sys.path.append("../common")
from MK_Common_Backup_Backblaze import *


class test_MK_Common_Backup_Backblaze_API:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_Backup_Backblaze.MK_Common_Backup_Backblaze_API()


    @classmethod
    def teardown_class(self):
        pass


    def test_MK_Common_Backup_Backblaze_Bucket_List(self):
        self.db.MK_Common_Backup_Backblaze_Bucket_List()


    @pytest.mark.parametrize(("bucket_name"), [
        ("bucket_upload"),
        ("bucket_test"),
        ("bucket_test")]) # for duplicate
    def test_MK_Common_Backup_Backblaze_Bucket_Create(self, bucket_name):
        MK_Common_Backup_Backblaze_Bucket_Create(bucket_name)


    @pytest.mark.parametrize(("file_name", "bucket_name", "file_password"), [
        ("./cache/HashCalc.txt", "bucket_upload", None),
        ("./cache/HashCalc.txt", "bucket_upload_fake", None),
        ("./cache/HashCalcfake.txt", "bucket_upload", None),
        ("./cache/HashCalc.txt", "bucket_test", "test")])
    def test_MK_Common_Backup_Backblaze_Upload_File(self, file_name, bucket_name, file_password):
        MK_Common_Backup_Backblaze_Upload_File(file_name, bucket_name, file_password)


    @pytest.mark.parametrize(("dir_name", "bucket_name", "dir_password"), [
        ("./cache", "bucket_upload", None),
        ("./cachefake", "bucket_upload_fake", None),
        ("./cache", "bucket_test", "test")])
    def test_MK_Common_Backup_Backblaze_Upload_Directory(self, dir_name, bucket_name,\
            dir_password=None):
        MK_Common_Backup_Backblaze_Upload_Directory(dir_name, bucket_name, dir_password)


    @pytest.mark.parametrize(("file_name", "local_file_name", "file_password"), [
        ("HashCalc.txt", "./cache/down.txt", None),
        ("hashCalc.txt", "./cache/down_pass.txt", "test")])
    def MK_Common_Backup_Backblaze_Download_File(self, file_name, local_file_name, file_password):
        MK_Common_Backup_Backblaze_Download_File(file_name, local_file_name, file_password)
        os.remove("./cache/down.txt")
        os.remove("./cache/down_pass.txt")

