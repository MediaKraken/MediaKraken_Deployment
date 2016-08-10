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


import pytest
import sys
sys.path.append("../MediaKraken_Common")
from MK_Common_Network_CIFS import *


class Test_MK_Common_CIFS_Share_URL_API:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_Network_CIFS.MK_Common_CIFS_Share_URL_API()


    @classmethod
    def teardown_class(self):
        pass


# def MK_Common_CIFS_URL_Director(self, connect_string):


# def MK_Common_CIFS_URL_Download(self, connect_string):


# def MK_Common_CIFS_URL_Upload(self, file_path, connect_string):


class Test_MK_Common_CIFS_Share_API:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_Network_CIFS.MK_Common_CIFS_Share_API()


    @classmethod
    def teardown_class(self):
        pass


# connect
# def MK_Common_CIFS_Connect(self, ip_addr, user_name='guest', user_password=''):


    # list shares
    def test_MK_Common_CIFS_Share_List_By_Connection(self):
        MK_Common_CIFS_Share_List_By_Connection()


# list files in share
# def MK_Common_CIFS_Share_File_List_By_Share(self, share_name, path_text='/'):


# verify smb directory
# def MK_Common_CIFS_Share_Directory_Check(self, share_name, dir_path):


# get specific path/file info
# def MK_Common_CIFS_Share_File_Dir_Info(self, share_name, file_path):


# upload file to smb
# def MK_Common_CIFS_Share_File_Upload(self, file_path):


# download from smb
# def MK_Common_CIFS_Share_File_Download(self, file_path):


# delete from smb
# def MK_Common_CIFS_Share_File_Delete(self, share_name, file_path):


    # close connection
    def test_MK_Common_CIFS_Close(self):
        MK_Common_CIFS_Close()


# cifs directory walk
# def MK_Common_CIFS_Walk(self, share_name, file_path=u'/'):
