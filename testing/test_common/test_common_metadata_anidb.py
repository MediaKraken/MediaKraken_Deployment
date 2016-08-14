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
from common_metadata_anidb import *


class TestCommonMetadataAnidb(object):


    @classmethod
    def setup_class(self):
        self.db_connection = database_base.common_metadata_anidb_API()


    @classmethod
    def teardown_class(self):
        pass


    # fetch the tarball of anime titles
    # def MK_Network_anidb_Fetch_Titles_File(self, data_type='dat'):


    # save anidb title data to database
    # def MK_Network_anidb_Save_Title_Data_To_DB(self, title_file):


    # find AID by title
    # def MK_Network_anidb_AID_by_Title(self, title_to_search):


    # remote api calls
    # def MK_Network_anidb_Connect(self, user_name, user_password):


    # logout of anidb
    def test_MK_Network_anidb_Logout(self):
        MK_Network_anidb_Logout()


    # close the anidb connect and stop the thread
    def test_MK_Network_anidb_Stop(self):
        MK_Network_anidb_Stop()

