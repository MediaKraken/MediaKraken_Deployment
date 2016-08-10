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
sys.path.append("../server") # for db import
import database as database_base


class Test_database_metadata_thesportsdb:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # select
    # def MK_Server_Database_MetadataTheSportsDB_Select_By_Guid(self, guid):
#         self.db.MK_Server_Database_Rollback()


    # insert
    # def MK_Server_Database_MetadataTheSportsDB_Insert(self, series_id_json, event_name, show_detail, image_json):
#         self.db.MK_Server_Database_Rollback()


    # updated
    # def MK_Server_Database_MetadataTheSports_Update(self, series_id_json, event_name, show_detail, sportsdb_id):
#         self.db.MK_Server_Database_Rollback()
