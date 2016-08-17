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
from common import common_network_cifs


class TestCommonCIFSShareURL(object):


    @classmethod
    def setup_class(self):
        self.db_connection = common_network_CIFS.com_cifs_Share_URL_API()


    @classmethod
    def teardown_class(self):
        pass


# def common_cifs_URL_Director(self, connect_string):


# def common_cifs_URL_Download(self, connect_string):


# def common_cifs_URL_Upload(self, file_path, connect_string):


class TestCommonCIFSShare(object):


    @classmethod
    def setup_class(self):
        self.db_connection = common_network_CIFS.com_cifs_Share_API()


    @classmethod
    def teardown_class(self):
        pass


# connect
# def common_cifs_Connect(self, ip_addr, user_name='guest', user_password=''):


    # list shares
    def test_common_cifs_Share_List_by_Connection(self):
        common_cifs_Share_List_by_Connection()


# list files in share
# def common_cifs_Share_File_List_by_Share(self, share_name, path_text='/'):


# verify smb directory
# def common_cifs_Share_Directory_Check(self, share_name, dir_path):


# get specific path/file info
# def common_cifs_Share_File_Dir_Info(self, share_name, file_path):


# upload file to smb
# def common_cifs_Share_File_Upload(self, file_path):


# download from smb
# def common_cifs_Share_File_Download(self, file_path):


# delete from smb
# def common_cifs_Share_File_Delete(self, share_name, file_path):


    # close connection
    def test_common_cifs_Close(self):
        common_cifs_Close()


# cifs directory walk
# def common_cifs_Walk(self, share_name, file_path='/'):
