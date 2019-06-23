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

import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
import database as database_base


class TestDatabaseCron:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_cron_list_count(self):
        """
        # return cron count
        """
        self.db_connection.db_rollback()
        self.db_connection.db_cron_list_count()

    def test_db_cron_list_count_false(self):
        """
        Test function
        """
        self.db_connection.db_rollback()
        self.db_connection.db_cron_list_count(False)

    def test_db_cron_list_count_true(self):
        """
        Test function
        """
        self.db_connection.db_rollback()
        self.db_connection.db_cron_list_count(True)

    @pytest.mark.parametrize(("enabled_only", "offset", "records"), [
        (False, None, None),
        (False, 100, 100),
        (False, 100000000, 1000),
        (True, None, None),
        (True, 100, 100),
        (True, 100000000, 1000)])
    def test_db_cron_list(self, enabled_only, offset, records):
        """
        # return cron list
        """
        self.db_connection.db_rollback()
        self.db_connection.db_cron_list(enabled_only, offset, records)

    @pytest.mark.parametrize(("cron_type"), [
        ('Game Audit'),
        ('fakecron')])
    def test_db_cron_time_update(self, cron_type):
        """
        # update cron run date
        """
        self.db_connection.db_rollback()
        self.db_connection.db_cron_time_update(cron_type)
