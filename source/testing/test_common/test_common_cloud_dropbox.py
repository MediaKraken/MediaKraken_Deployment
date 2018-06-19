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
from common import common_cloud_dropbox
from common import common_config_ini


class TestCommonDropBox(object):

    @classmethod
    def setup_class(self):
        # open the database
        option_config_json, db_connection = common_config_ini.com_config_read(db_prod=False)
        self.dropbox_connection = common_cloud_dropbox.CommonCloudDropbox(
            option_config_json)

    @classmethod
    def teardown_class(self):
        pass

    def test_dropbox_user_auth(self):
        """
        Test function
        """
        self.dropbox_connection.dropbox_user_auth()

    @pytest.mark.parametrize(("file_name", "file_save_name"), [
        ("./cache/HashCalc.txt", "HashCalc.txt"),
        ("./cache/HashCalcfake.txt", "HashCalcfake.txt")])
    def test_dropbox_upload(self, file_name, file_save_name):
        """
        Test function
        """
        self.dropbox_connection.dropbox_upload(file_name, file_save_name)

    @pytest.mark.parametrize(("dir_name"), [
        ("/"),
        ("metaman"),
        ("fakedir")])
    def test_dropbox_list(self, dir_name):
        """
        Test function
        """
        self.dropbox_connection.dropbox_list(dir_name)

    @pytest.mark.parametrize(("file_name", "file_save_name"), [
        ("HashCalc.txt", "./cache/HashCalcDown.txt"),
        ("HashCalcfake.txt", "./cache/HashCalcDown2.txt")])
    def test_dropbox_download(self, file_name, file_save_name):
        """
        Test function
        """
        self.dropbox_connection.dropbox_download(file_name, file_save_name)
