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


class TestDatabaseOptionStatus(object):


    @classmethod
    def setup_class(self):
        self.db = database_base.MKServerDatabase()
        self.db.srv_db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.srv_db_close()


    def test_srv_db_option_status_read(self):
        self.db.srv_db_option_status_read()
        self.db.srv_db_rollback()


    # def srv_db_option_status_update(self, option_json, status_json):
#        self.db.srv_db_rollback()


    # def srv_db_option_status_update_scan_json(self, scan_json):
#        self.db.srv_db_rollback()


    # def srv_db_option_status_update_scan_json_rec(self, dir_path, scan_status, scan_percent):
#         self.db.srv_db_rollback()
