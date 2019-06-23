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

import json
import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
import database as database_base


class TestDatabaseReview:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    @pytest.mark.parametrize(("metadata_id"), [
        ('ea0e5d88-4c7d-4c2b-b8df-6112a41ee776'),  # fake id
        ('ea0e5d88-4c7d-4c2b-b8df-6112a41ee776')])  # TODO real one
    def test_db_review_count(self, metadata_id):
        """
        # count reviews for media
        """
        self.db_connection.db_rollback()
        self.db_connection.db_review_count(metadata_id)

    @pytest.mark.parametrize(("metadata_id"), [
        ('ea0e5d88-4c7d-4c2b-b8df-6112a41ee776'),  # fake id
        ('ea0e5d88-4c7d-4c2b-b8df-6112a41ee776')])  # TODO real one
    def test_db_review_list_by_tmdb_guid(self, metadata_id):
        """
        # grab reviews for metadata
        """
        self.db_connection.db_rollback()
        self.db_connection.db_review_list_by_tmdb_guid(metadata_id)

    @pytest.mark.parametrize(("metadata_id", "review_json"), [
        (json.dumps({'themoviedb': 3}), json.dumps({'test': 123})),  # fake id
        (json.dumps({'themoviedb': 3}), json.dumps({'test2': 1323233}))])  # TODO real one
    def test_db_review_insert(self, metadata_id, review_json):
        """
        # insert record
        """
        self.db_connection.db_rollback()
        self.db_connection.db_review_insert(metadata_id, review_json)
