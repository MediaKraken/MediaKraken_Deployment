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
sys.path.append('.')
import database as database_base


class TestDatabaseNas(object):


    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()


    def test_db_nas_count(self):
        """
        # count nas
        """
        self.db_connection.db_nas_count()


    def test_db_nas_list(self):
        """
        # read nas
        """
        self.db_connection.db_nas_list()


#    def db_nas_insert(self, nas_json):
#        """
#        # insert record
#        """
#
#
#    def db_nas_update(self, guid, nas_json):
#        """
#        # update record
#        """
#
#
#    def db_nas_delete(self, guid):
#        """
#        # delete record
#        """
#
#
#    def db_nas_read(self, guid):
#        """
#        # find details by nas
#        """
