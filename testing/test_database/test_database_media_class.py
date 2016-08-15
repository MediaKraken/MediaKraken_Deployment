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
sys.path.append("./common")
sys.path.append("./server") # for db import
import database as database_base


class TestDatabaseMediaClass(object):


    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.srv_db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db_connection.srv_db_close()


    def test_srv_db_media_class_list_count(self):
        """
        # count media class
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_class_list_count()


    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100,100),
        (100000000,1000)])
    def test_srv_db_media_class_list(self, offset, records):
        """
        # list media class
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_class_list(offset, records)


    @pytest.mark.parametrize(("class_uuid"), [
        ('928c56c3-253d-4e30-924e-5698be6d3d39'),   # exist
        ('928c56c3-253d-4e30-924e-5698be6d3d37')])  # not exist
    def test_srv_db_media_class_by_uuid(self, class_uuid):
        """
        # find the class text by uuid
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_class_by_uuid(class_uuid)


    @pytest.mark.parametrize(("class_text"), [
        ('Movie'),
        ('fakestuff')])
    def test_srv_db_media_uuid_by_class(self, class_text):
        """
        # find the class uuid by class text
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_uuid_by_class(class_text)
