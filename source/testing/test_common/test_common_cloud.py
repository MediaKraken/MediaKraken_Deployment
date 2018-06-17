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

import pytest  # pylint: disable=W0611

sys.path.append('.')
from common import common_cloud
from common import common_config_ini


class TestCommonCloud(object):

    @classmethod
    def setup_class(self):
        # open the database
        option_config_json, db_connection = common_config_ini.com_config_read(db_prod=False)
        self.cloud_handle = common_cloud.CommonCloud(option_config_json)

    @classmethod
    def teardown_class(self):
        pass

    # get list of all backups
    def test_common_cloud_backup_list(self):
        """
        Test function
        """
        self.cloud_handle.com_cloud_backup_list()

    # store file in cloud
    # def common_cloud_File_Store(self, cloud_type, file_path_name, file_save_name, backup_bucket=False):

    # delete file in cloud
    # def common_cloud_File_Delete(self, cloud_type, file_name, backup_bucket=False):

    # list files in cloud
    # def common_cloud_File_List(self, cloud_type, file_path=None, backup_bucket=False):

    # fetch file from cloud
    # def common_cloud_File_Retrieve(self, cloud_type, file_name, file_location):

    # rename file on cloud
    # def common_cloud_File_Rename(self, cloud_type, file_from, file_to):

    # create direcgtory in cloud
    @pytest.mark.parametrize(("cloud_type", "dir_name"), [
        ("awss3", "dir_test"),
        ("awss3", "dir_test"),  # dupe test
        ("dropbox", "dir_test"),
        ("dropbox", "dir_test"),  # dupe test
        ("google", "dir_test"),
        ("google", "dir_test"),  # dupe test
        ("local", "dir_test"),
        ("local", "dir_test"),  # dupe test
        ("onedrive", "dir_test"),
        ("onedrive", "dir_test")])  # dupe test
    def test_common_cloud_create_folder(self, cloud_type, dir_name):
        """
        Test function
        """
        self.cloud_handle.com_cloud_create_folder(cloud_type, dir_name)
