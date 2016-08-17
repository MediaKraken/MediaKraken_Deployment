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


class TestDatabaseMetadata_book(object):


    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.srv_db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db_connection.srv_db_close()


    # metadata guid by isbm id
    # def srv_db_metabook_guid_by_isbn(self, isbn_uuid, isbn13_uuid):
#        self.db_connection.srv_db_rollback()


    # metadata guid by name
    # def srv_db_metabook_guid_by_name(self, book_name):
#        self.db_connection.srv_db_rollback()


    # insert metadata json from isbndb
    # def srv_db_metabook_book_insert(self, json_data):
#        self.db_connection.srv_db_rollback()
