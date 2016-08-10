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
sys.path.append("../MediaKraken_Server")  # for db import
import database as database_base


class Test_database_activity:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # def MK_Server_Database_Activity_Insert(self, activity_name, activity_overview, activity_short_overview, activity_type, activity_itemid, activity_userid, activity_log_severity):
    # TODO
#        self.db.MK_Server_Database_Rollback()


    @pytest.mark.parametrize(("days_old"), [
        (7),
        (400)])
    def test_MK_Server_Database_Activity_Purge(self, days_old):
        self.db.MK_Server_Database_Activity_Purge(days_old)
        self.db.MK_Server_Database_Rollback()
