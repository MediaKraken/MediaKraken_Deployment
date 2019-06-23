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


class TestDatabaseMetadataMovie:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    @pytest.mark.parametrize(("metadata_guid", "user_id", "status_text"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, 'watched'),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, 'watched'),  # not found
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, 'watched'),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, 'watched')])  # not found
    def test_db_meta_movie_status_update(self, metadata_guid, user_id, status_text):
        """
        # set favorite status for media
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_movie_status_update(
            metadata_guid, user_id, status_text)
