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

import os
import sys

import pytest

sys.path.append('.')
from common import common_backup_backblaze


class TestCommonBackupBackblaze(object):
    """
    Test backblaze
    """

    @classmethod
    def setup_class(self):
        self.backblaze_connection = common_backup_backblaze.CommonBackupBackblaze()

    @classmethod
    def teardown_class(self):
        pass

    def test_com_backup_backblaze_bucket_list(self):
        """
        Test bucket list
        """
        self.backblaze_connection.com_backblaze_bucket_list()

    @pytest.mark.parametrize(("bucket_name"), [
        ("bucket_upload"),
        ("bucket_test"),
        ("bucket_test")])  # for duplicate
    def test_com_backup_backblaze_bucket_create(self, bucket_name):
        """
        Test function
        """
        self.backblaze_connection.com_backblaze_bucket_create(bucket_name)

    @pytest.mark.parametrize(("file_name", "bucket_name", "file_password"), [
        ("./cache/HashCalc.txt", "bucket_upload", None),
        ("./cache/HashCalc.txt", "bucket_upload_fake", None),
        ("./cache/HashCalcfake.txt", "bucket_upload", None),
        ("./cache/HashCalc.txt", "bucket_test", "test")])
    def test_com_backup_backblaze_upload_file(self, file_name, bucket_name, file_password):
        """
        Test function
        """
        self.backblaze_connection.com_backblaze_upload_file(file_name, bucket_name,
                                                            file_password)

    @pytest.mark.parametrize(("dir_name", "bucket_name", "dir_password"), [
        ("./cache", "bucket_upload", None),
        ("./cachefake", "bucket_upload_fake", None),
        ("./cache", "bucket_test", "test")])
    def test_com_backup_backblaze_upload_directory(self, dir_name, bucket_name,
                                                   dir_password):
        """
        Test function
        """
        self.backblaze_connection.com_backblaze_upload_directory(dir_name, bucket_name,
                                                                 dir_password)

    @pytest.mark.parametrize(("file_name", "local_file_name", "file_password"), [
        ("HashCalc.txt", "./cache/down.txt", None),
        ("hashCalc.txt", "./cache/down_pass.txt", "test")])
    def test_com_backup_backblaze_download_file(self, file_name, local_file_name, file_password):
        """
        Test function
        """
        self.backblaze_connection.com_backblaze_download_file(file_name, local_file_name,
                                                              file_password)
        os.remove("./cache/down.txt")
        os.remove("./cache/down_pass.txt")
