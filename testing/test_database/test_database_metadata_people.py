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
import database as database_base


class TestDatabaseMetadataPeople(object):


    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.srv_db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db_connection.srv_db_close()


    def test_srv_db_meta_person_list_count(self):
        """
        # count person metadata
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_meta_person_list_count()


    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_srv_db_meta_person_list(self, offset, records):
        """
        # return list of people
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_meta_person_list(offset, records)


    # return person data
    # def srv_db_meta_person_by_guid(self, guid):
#         self.db_connection.srv_db_rollback()


    # return person data by name
    # def srv_db_meta_person_by_name(self, person_name):
#         self.db_connection.srv_db_rollback()


    # does person exist already by host/id
    # def srv_db_meta_person_id_count(self, host_type, guid):
#         self.db_connection.srv_db_rollback()


    # insert person
    # def srv_db_metdata_person_insert(self, person_name, media_id_json, person_json, image_json=None):
#         self.db_connection.srv_db_rollback()


    # batch insert from json of crew/cast
    # def srv_db_meta_person_insert_cast_crew(self, meta_type, person_json):
#         self.db_connection.srv_db_rollback()


    # find other media for person
    # def srv_db_meta_person_as_seen_in(self, person_guid):
#         self.db_connection.srv_db_rollback()
