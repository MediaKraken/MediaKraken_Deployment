"""
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
"""

import json
import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
import database_async as database_base


class TestDatabaseLink:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)
        self.new_guid = None

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_link_list_count(self):
        """
        Test function
        """
        self.db_connection.db_rollback()
        self.db_connection.db_link_list_count()

    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_link_list(self, offset, records):
        """
        # return list of sync jobs
        """
        self.db_connection.db_rollback()
        self.db_connection.db_link_list(offset, records)

    def test_db_link_insert(self):
        """
        # insert link job
        """
        self.db_connection.db_rollback()
        self.new_guid = self.db_connection.db_link_insert(
            json.dumps({'test': 'stuff'}))
        self.db_connection.db_commit()

    def test_db_link_delete(self):
        """
        # delete link job
        """
        self.db_connection.db_rollback()
        self.db_connection.db_link_delete(self.new_guid)
        self.db_connection.db_commit()
