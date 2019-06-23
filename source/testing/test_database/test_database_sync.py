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


class TestDatabaseSync:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_sync_list_count(self):
        """
        # return count of sync jobs
        """
        self.db_connection.db_rollback()
        self.db_connection.db_sync_list_count()

    @pytest.mark.parametrize(("offset", "records", "user_guid"), [
        (None, None, None),
        (100, 100, None),
        (100000000, 1000, None),
        (None, None, 1),
        (100, 100, 1),
        (100000000, 1000, 1)])
    def test_db_sync_list(self, offset, records, user_guid):
        """
        # return list of sync jobs
        """
        self.db_connection.db_rollback()
        self.db_connection.db_sync_list(offset, records, user_guid)

    # insert sync job
    # def db_sync_insert(self, sync_path, sync_path_to, sync_json):
#        self.db_connection.db_rollback()


# update progress
# def db_sync_progress_update(self, sync_guid, sync_percent):
#        self.db_connection.db_rollback()


# delete sync job
# def db_sync_delete(self, sync_guid):
#        self.db_connection.db_rollback()
