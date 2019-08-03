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
from common import common_network_cifs


class TestCommonCIFSShareURL:

    @classmethod
    def setup_class(self):
        self.db_connection = common_network_cifs.CommonNetworkCIFSShareURL()

    @classmethod
    def teardown_class(self):
        pass


# def common_cifs_URL_Director(self, connect_string):


# def common_cifs_URL_Download(self, connect_string):


# def common_cifs_URL_Upload(self, file_path, connect_string):


class TestCommonCIFSShare:

    @classmethod
    def setup_class(self):
        self.db_connection = common_network_cifs.CommonCIFSShare()

    @classmethod
    def teardown_class(self):
        pass

    # connect
    # def com_cifs_Connect(self, ip_addr, user_name='guest', user_password=''):

    # list shares
    # def test_com_cifs_share_list_by_connection(self):
    #     """
    #     Test function
    #     """
    #     self.db_connection.com_cifs_share_list_by_connection()

    # list files in share
    # def com_cifs_Share_File_List_by_Share(self, share_name, path_text='/'):

    # verify smb directory
    # def com_cifs_Share_Directory_Check(self, share_name, dir_path):

    # get specific path/file info
    # def com_cifs_Share_File_Dir_Info(self, share_name, file_path):

    # upload file to smb
    # def com_cifs_Share_File_Upload(self, file_path):

    # download from smb
    # def com_cifs_Share_File_Download(self, file_path):

    # delete from smb
    # def com_cifs_Share_File_Delete(self, share_name, file_path):

    # close connection
    # def test_com_cifs_close(self):
    #     """
    #     Test function
    #     """
    #     self.db_connection.com_cifs_close()

# cifs directory walk
# def com_cifs_Walk(self, share_name, file_path='/'):
