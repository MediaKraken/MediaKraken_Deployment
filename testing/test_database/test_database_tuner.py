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
import json
import sys

sys.path.append('.')
import pytest  # pylint: disable=W0611
import database as database_base


class TestDatabaseTuner(object):

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)
        self.new_guid = None

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_tuner_count(self):
        """
        # count tuners
        """
        self.db_connection.db_rollback()
        self.db_connection.db_tuner_count()

    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_tuner_list(self, offset, records):
        """
        # read tuners
        """
        self.db_connection.db_rollback()
        self.db_connection.db_tuner_list(offset, records)

    def test_db_tuner_insert(self):
        """
        # insert record
        """
        self.db_connection.db_rollback()
        self.new_guid = self.db_connection.db_tuner_insert(json.dumps({'ID': 'test'}))

    def test_db_tuner_update(self):
        """
        # update record
        """
        self.db_connection.db_rollback()
        self.db_connection.db_tuner_update(self.new_guid, json.dumps({'ID': 'test2'}))
        self.db_connection.db_commit()

    def test_db_tuner_by_serial(self):
        """
        # find detials by hardware id (serial)
        """
        self.db_connection.db_rollback()
        self.db_connection.db_tuner_by_serial('test2')

    def test_db_tuner_delete(self):
        """
        # delete record
        """
        self.db_connection.db_rollback()
        self.db_connection.db_tuner_delete(self.new_guid)
        self.db_connection.db_commit()
