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


class TestDatabaseNotification:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)
        self.new_guid = None

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    @pytest.mark.parametrize(("notification_data", "notification_dismissable"), [
        ('Test Notice', True),
        ('Test nondismiss', False)])
    # insert notifications
    def test_db_notification_insert(self, notification_data, notification_dismissable):
        """
        Test notice insert
        """
        self.db_connection.db_rollback()
        self.new_guid = self.db_connection.db_notification_insert(notification_data,
                                                                  notification_dismissable)

    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_notification_read(self, offset, records):
        """
        # read all notifications
        """
        self.db_connection.db_rollback()
        self.db_connection.db_notification_read(offset, records)

    def test_db_notification_delete(self):
        """
        # remove noticications
        """
        self.db_connection.db_rollback()
        self.db_connection.db_notification_delete(self.new_guid)
        self.db_connection.db_commit()
