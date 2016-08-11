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
sys.path.append("./common")
sys.path.append("./server") # for db import
import database as database_base


class Test_database_cron:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # return cron count
    def test_MK_Server_Database_Cron_List_Count(self):
        self.db.MK_Server_Database_Cron_List_Count()
        self.db.MK_Server_Database_Rollback()


    def test_MK_Server_Database_Cron_List_Count_False(self):
        self.db.MK_Server_Database_Cron_List_Count(False)
        self.db.MK_Server_Database_Rollback()


    def test_MK_Server_Database_Cron_List_Count_True(self):
        self.db.MK_Server_Database_Cron_List_Count(True)
        self.db.MK_Server_Database_Rollback()


    # return cron list
    @pytest.mark.parametrize(("enabled_only", "offset", "records"), [
        (False, None, None),
        (False, 100, 100),
        (False, 100000000, 1000),
        (True, None, None),
        (True, 100, 100),
        (True, 100000000, 1000)])
    def test_MK_Server_Database_Cron_List(self, enabled_only, offset, records):
        self.db.MK_Server_Database_Cron_List(enabled_only, offset, records)
        self.db.MK_Server_Database_Rollback()


    # update cron run date
    # def MK_Server_Database_Cron_Time_Update(self, cron_type):
#        self.db.MK_Server_Database_Rollback()
