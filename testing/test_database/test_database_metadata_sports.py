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


class TestDatabaseMetadataSports(object):


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.srv_db_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.srv_db_Close()


    # metadata guid by imdb id
    # def srv_db_meta_Sports_GUID_By_thesportsdb(self, thesports_uuid):
#        self.db.srv_db_Rollback()


    def Test_srv_db_meta_sports_list_count(self):
        self.db.srv_db_meta_sports_list_count()
        self.db.srv_db_Rollback()


    # return list of game systems
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_srv_db_meta_sports_list(self, offset, records):
        self.db.srv_db_meta_sports_list(offset, records)
        self.db.srv_db_Rollback()


    # fetch guid by event name
    # def srv_db_meta_sports_guid_by_event_name(self, event_name):
#        self.db.srv_db_Rollback()
