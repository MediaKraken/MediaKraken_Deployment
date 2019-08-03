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


class TestDatabaseMediaClass:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_media_class_list_count(self):
        """
        # count media class
        """
        self.db_connection.db_rollback()
        self.db_connection.db_media_class_list_count()

    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_media_class_list(self, offset, records):
        """
        # list media class
        """
        self.db_connection.db_rollback()
        self.db_connection.db_media_class_list(offset, records)

    @pytest.mark.parametrize(("class_uuid"), [
        ('928c56c3-253d-4e30-924e-5698be6d3d39'),  # exist
        ('928c56c3-253d-4e30-924e-5698be6d3d37')])  # not exist
    def test_db_media_class_by_uuid(self, class_uuid):
        """
        # find the class text by uuid
        """
        self.db_connection.db_rollback()
        self.db_connection.db_media_class_by_uuid(class_uuid)

    @pytest.mark.parametrize(("class_text"), [
        ('Movie'),
        ('fakestuff')])
    def test_db_media_uuid_by_class(self, class_text):
        """
        # find the class uuid by class text
        """
        self.db_connection.db_rollback()
        self.db_connection.db_media_uuid_by_class(class_text)
