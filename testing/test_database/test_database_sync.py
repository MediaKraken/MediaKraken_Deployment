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


class TestDatabaseSync(object):


    @classmethod
    def setup_class(self):
        self.db = database_base.MKServerDatabase()
        self.db.srv_db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.srv_db_close()


    # return count of sync jobs
    def srv_db_Sync_List_Count(self):
        self.db.srv_db_Sync_List_Count()
        self.db.srv_db_rollback()


    # return list of sync jobs
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_srv_db_Sync_List(self, offset, records):
        self.db.srv_db_Sync_List(offset, records)
        self.db.srv_db_rollback()


    # insert sync job
    # def srv_db_Sync_Insert(self, sync_path, sync_path_to, sync_json):
#        self.db.srv_db_rollback()


    # delete sync job
    # def srv_db_Sync_Delete(self, sync_guid):
#        self.db.srv_db_rollback()


    # update progress
    # def srv_db_Sync_Progress_Update(self, sync_guid, sync_percent):
#        self.db.srv_db_rollback()
