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
import sys

sys.path.append('.')
import database as database_base


class TestDatabaseTriggers(object):

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)
        self.new_guid = None

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_trigger_insert(self):
        """
        # create/insert a trigger
        """
        self.db_connection.db_rollback()
        self.new_guid = self.db_connection.db_trigger_insert(('ls', '-al'))

    def test_db_triggers_read(self):
        """
        # read the triggers
        """
        self.db_connection.db_rollback()
        self.db_connection.db_triggers_read()

    def test_db_triggers_delete(self):
        """
        # remove trigger
        """
        self.db_connection.db_rollback()
        self.db_connection.db_triggers_delete(self.new_guid)
