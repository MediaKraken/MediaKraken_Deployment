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


class TestDatabaseMetadataPeople:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_meta_person_list_count(self):
        """
        # count person metadata
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_person_list_count()

    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_meta_person_list(self, offset, records):
        """
        # return list of people
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_person_list(offset, records)

    @pytest.mark.parametrize(("guid"), [
        ('b5dbb1f7-f172-4d04-897d-f925f2200f8f'),
        ('7191eeb2-1dd6-4ed8-9558-ad18e8f9467c')])  # TODO real id
    def test_db_meta_person_by_guid(self, guid):
        """
        # return person data
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_person_by_guid(guid)

    @pytest.mark.parametrize(("person_name"), [
        ('fakename'),
        ('fakename2')])  # TODO real name
    def test_db_meta_person_by_name(self, person_name):
        """
        # return person data by name
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_person_by_name(person_name)

    @pytest.mark.parametrize(("host_type", "guid", "expected_result"), [
        ('themoviedb', 169, 0),  # TODO set back to 1 with real id
        ('fake', 1000, 0)])
    def test_db_meta_person_id_count(self, host_type, guid, expected_result):
        """
        # does person exist already by host/id
        """
        self.db_connection.db_rollback()
        assert self.db_connection.db_meta_person_id_count(
            host_type, guid) == expected_result

    # insert person
    # def db_metdata_person_insert(self, person_name, media_id_json, person_json, image_json=None):
    #         self.db_connection.db_rollback()

    # batch insert from json of crew/cast
    # def db_meta_person_insert_cast_crew(self, meta_type, person_json):
    #         self.db_connection.db_rollback()

    @pytest.mark.parametrize(("person_guid"), [
        ('b5dbb1f7-f172-4d04-897d-f925f2200f8f'),
        ('7191eeb2-1dd6-4ed8-9558-ad18e8f9467c')])  # TODO real id
    def test_db_meta_person_as_seen_in(self, person_guid):
        """
        # find other media for person
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_person_as_seen_in(person_guid)
