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
sys.path.append("../common")
from MK_Common_Database_Octmote import *


class Test_common_database_octmote:


    @classmethod
    def setup_class(self):
        self.db = MK_Database_Sqlite3_Open(None):


    @classmethod
    def teardown_class(self):
        self.db.MK_Database_Sqlite3_Close()


# insert new layout config into database
#def MK_Database_Sqlite3_Layout_Config_Insert(layout_record_name, layout_record_json):


    def test_MK_Database_Sqlite3_Layout_List(self):
        MK_Database_Sqlite3_Layout_List()


#def MK_Database_Sqlite3_Layout_Detail(guid):


# insert new device type into database
#def MK_Database_Sqlite3_Device_Insert(device_record_name, device_record_description):


    def test_MK_Database_Sqlite3_Device_List(self):
        self.db.MK_Database_Sqlite3_Device_List()


#def MK_Database_Sqlite3_Device_Detail(guid):


# insert new item into database
#def MK_Database_Sqlite3_Item_Insert(item_record_json):


    def test_MK_Database_Sqlite3_Item_List(self):
        self.db.MK_Database_Sqlite3_Item_List()


#def MK_Database_Sqlite3_Item_Detail(guid):


# do general query
#def MK_Database_Sqlite3_General_Query(sql_command):


# do general insert
#def MK_Database_Sqlite3_General_Insert(sql_command):


# insert new anidb entries into database
#def MK_Database_Sqlite3_AniDB_Title_Insert(sql_params_list):


#def MK_Database_Sqlite3_AniDB_Title_Search(title_to_search):
