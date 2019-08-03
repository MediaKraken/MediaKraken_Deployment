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

sys.path.append('.')
import database as database_base


class TestDatabaseOptionStatus:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_opt_status_read(self):
        """
        Test function
        """
        self.db_connection.db_rollback()
        self.db_connection.db_opt_status_read()

    # def db_opt_status_update(self, option_json, status_json):
#        self.db_connection.db_rollback()


# def db_opt_status_update_scan(self, scan_json):
#        self.db_connection.db_rollback()


# def db_opt_status_update_scan_rec(self, dir_path, scan_status, scan_percent):
#         self.db_connection.db_rollback()
