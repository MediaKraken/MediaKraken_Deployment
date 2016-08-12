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
sys.path.append("./common")
sys.path.append("./server") # for db import
import database as database_base


class Test_database_metadata_games:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # return game system data
    # def MK_Server_Database_Metadata_Game_System_By_GUID(self, guid):
#        self.db.MK_Server_Database_Rollback()


    # def MK_Server_Database_Metadata_Game_System_List_Count(self):
    def Test_MK_Server_Database_Metadata_Game_System_List_Count(self):
        self.db.MK_Server_Database_Metadata_Game_System_List_Count()
        self.db.MK_Server_Database_Rollback()


    # return list of game systems
    # def MK_Server_Database_Metadata_Game_System_List(self, offset=None, records=None):
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_MK_Server_Database_Metadata_Game_System_List(self, offset, records):
        self.db.MK_Server_Database_Metadata_Game_System_List(offset, records)
        self.db.MK_Server_Database_Rollback()


    # return list of games count
    # def MK_Server_Database_Metadata_Game_List_Count(self):
    def Test_MK_Server_Database_Metadata_Game_List_Count(self):
        self.db.MK_Server_Database_Metadata_Game_List_Count()
        self.db.MK_Server_Database_Rollback()


    # return list of games
    # def MK_Server_Database_Metadata_Game_List(self, offset=None, records=None):
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_MK_Server_Database_Metadata_Game_List(self, offset, records):
        self.db.MK_Server_Database_Metadata_Game_List(offset, records)
        self.db.MK_Server_Database_Rollback()


    # return game data
    # def MK_Server_Database_Metadata_Game_By_GUID(self, guid):
#        self.db.MK_Server_Database_Rollback()


    # game list by system count
    # def MK_Server_Database_Metadata_Game_By_System_Count(self, guid):
#        self.db.MK_Server_Database_Rollback()


    # game list by system count
    # def MK_Server_Database_Metadata_Game_By_System(self, guid, offset=None, records=None):
#        self.db.MK_Server_Database_Rollback()


    # game by sha1
    # def MK_Server_Database_Metadata_Game_By_SHA1(self, sha1_hash):
#        self.db.MK_Server_Database_Rollback()


    # game by name and system short name
    # def MK_Server_Database_Metadata_Game_By_Name_And_System(self, game_name, game_system_short_name):
#        self.db.MK_Server_Database_Rollback()
