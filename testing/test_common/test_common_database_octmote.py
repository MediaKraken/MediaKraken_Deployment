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
from com_Database_Octmote import *


class TestCommonDatabaseOctmote(object):


    @classmethod
    def setup_class(self):
        self.db_connection.connection = com_db_Open(None):


    @classmethod
    def teardown_class(self):
        self.db_connection.com_db_Close()


# insert new layout config into database
#def com_db_Layout_Config_Insert(layout_record_name, layout_record_json):


    def test_com_db_Layout_List(self):
        com_db_Layout_List()


#def com_db_Layout_Detail(guid):


# insert new device type into database
#def com_db_Device_Insert(device_record_name, device_record_description):


    def test_com_db_Device_List(self):
        self.db_connection.com_db_Device_List()


#def com_db_Device_Detail(guid):


# insert new item into database
#def com_db_Item_Insert(item_record_json):


    def test_com_db_Item_List(self):
        self.db_connection.com_db_Item_List()


#def com_db_Item_Detail(guid):


# do general query
#def com_db_General_Query(sql_command):


# do general insert
#def com_db_General_Insert(sql_command):


# insert new anidb entries into database
#def com_db_anidb_Title_Insert(sql_params_list):


#def com_db_anidb_Title_Search(title_to_search):
