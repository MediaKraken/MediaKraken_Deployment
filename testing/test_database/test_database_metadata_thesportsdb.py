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
import pytest # pylint: disable=W0611
import sys
sys.path.append('.')
import database as database_base


class TestDatabaseMetadataThesportsdb(object):


    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()


    # select
    # def db_metathesportsdb_select_guid(self, guid):
#         self.db_connection.db_rollback()


    # insert
    # def db_metathesportsdb_insert(self, series_id_json, event_name, show_detail, image_json):
#         self.db_connection.db_rollback()


    # updated
    # def db_metathesports_update(self, series_id_json, event_name, show_detail, sportsdb_id):
#         self.db_connection.db_rollback()
