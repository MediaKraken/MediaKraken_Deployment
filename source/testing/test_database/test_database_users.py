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


class TestDatabaseUsers:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_user_list_name_count(self):
        """
        # return user count
        """
        self.db_connection.db_rollback()
        self.db_connection.db_user_list_name_count()

    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_user_list_name(self, offset, records):
        """
        # return user list
        """
        self.db_connection.db_rollback()
        self.db_connection.db_user_list_name(offset, records)

    @pytest.mark.parametrize(("guid"), [
        (1),
        (923894894893)])  # not exist
    def test_db_user_detail(self, guid):
        """
        # return all data for specified user
        """
        self.db_connection.db_rollback()
        self.db_connection.db_user_detail(guid)

    @pytest.mark.parametrize(("user_guid"), [
        (1),
        (923894894893)])  # not exist
    def test_db_user_delete(self, user_guid):
        """
        # remove user
        """
        self.db_connection.db_rollback()
        self.db_connection.db_user_delete(user_guid)
        self.db_connection.db_rollback()

    # verify user logon
    # def db_user_login_kodi(self, user_data):
#        self.db_connection.db_rollback()
