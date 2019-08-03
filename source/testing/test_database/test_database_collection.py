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


class TestDatabaseCollection:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    # find all known media
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_collection_list(self, offset, records):
        """
        Test function
        """
        self.db_connection.db_rollback()
        self.db_connection.db_collection_list(offset, records)

    # read collection data from json metadata
    def test_db_media_collection_scan(self):
        """
        Test function
        """
        self.db_connection.db_rollback()
        self.db_connection.db_media_collection_scan()

    # find guid of collection name
    @pytest.mark.parametrize(("collection_name"), [
        ('Darko Collection'),
        ('fakecollectionstuff')])
    def test_db_collection_guid_by_name(self, collection_name):
        """
        Test function
        """
        self.db_connection.db_rollback()
        self.db_connection.db_collection_guid_by_name(collection_name)

    @pytest.mark.parametrize(("tmdb_id"), [
        (393379),
        (2)])  # fake id
    def test_db_collection_by_tmdb(self, tmdb_id):
        """
        # find guid of collection id
        """
        self.db_connection.db_rollback()
        self.db_connection.db_collection_by_tmdb(tmdb_id)

    # insert collection
    # def db_collection_insert(self, collection_name, guid_json, metadata_json, localimage_json):
#        self.db_connection.db_rollback()


# update collection ids
# def db_collection_update(self, collection_guid, guid_json):
#        self.db_connection.db_rollback()


# pull in colleciton info
# def db_collection_read_by_guid(self, media_uuid):
#        self.db_connection.db_rollback()
