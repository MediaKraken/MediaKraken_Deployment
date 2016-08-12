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


class test_database_tuner:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # count tuners
    def test_MK_Server_Database_Tuner_Count(self):
        self.db.MK_Server_Database_Tuner_Count()
        self.db.MK_Server_Database_Rollback()


    # read tuners
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_MK_Server_Database_Tuner_List(self, offset, records):
        self.db.MK_Server_Database_Tuner_List(offset, records)
        self.db.MK_Server_Database_Rollback()


    # insert record
    # def MK_Server_Database_Tuner_Insert(self, tuner_json):
#        self.db.MK_Server_Database_Rollback()


    # update record
    # def MK_Server_Database_Tuner_Update(self, guid, tuner_json):
#        self.db.MK_Server_Database_Rollback()


    # delete record
    # def MK_Server_Database_Tuner_Delete(self, guid):
#        self.db.MK_Server_Database_Rollback()


    # find detials by hardware id (serial)
    # def MK_Server_Database_Tuner_By_Serial(self, serial_no):
#         self.db.MK_Server_Database_Rollback()
