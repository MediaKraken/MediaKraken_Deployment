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
sys.append('.')
import database as database_base


class TestDatabaseActivity(object):


    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()


    # def db_activity_insert(self, activity_name, activity_overview, \
#activity_short_overview, activity_type, activity_itemid, activity_userid, activity_log_severity):
    # TODO
#        self.db_connection.db_rollback()


    @pytest.mark.parametrize(("days_old"), [
        (7),
        (400)])
    def test_db_activity_purge(self, days_old):
        """
        Test function
        """
        self.db_connection.db_rollback()
        self.db_connection.db_activity_purge(days_old)
