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
import pytest  # pylint: disable=W0611
import json
import sys

sys.path.append('.')
import database as database_base


class TestDatabaseNas(object):

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)
        self.new_guid = None

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_nas_count(self):
        """
        # count nas
        """
        self.db_connection.db_rollback()
        self.db_connection.db_nas_count()

    def test_db_nas_list(self):
        """
        # read nas
        """
        self.db_connection.db_rollback()
        self.db_connection.db_nas_list()

    @pytest.mark.parametrize(("nas_json"), [
        (json.dumps({'Nas': 234}))])
    def test_db_nas_insert(self, nas_json):
        """
        # insert record
        """
        self.db_connection.db_rollback()
        self.new_guid = self.db_connection.db_nas_insert(nas_json)

    def test_db_nas_update(self):
        """
        # update record
        """
        self.db_connection.db_rollback()
        self.db_connection.db_nas_update(self.new_guid, json.dumps({'Nas': 484884}))
        self.db_connection.db_commit()

    def test_db_nas_read(self):
        """
        # find details by nas
        """
        self.db_connection.db_rollback()
        self.db_connection.db_nas_read(self.new_guid)

    def test_db_nas_delete(self):
        """
        # delete record
        """
        self.db_connection.db_rollback()
        self.db_connection.db_nas_delete(self.new_guid)
        self.db_connection.db_commit()
