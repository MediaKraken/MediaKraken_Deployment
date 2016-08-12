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


class TestDatabaseDevices(object):


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.srv_db_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.srv_db_Close()


    # count device
    def Test_srv_db_Device_Count(self):
        self.db.srv_db_Device_Count()
        self.db.srv_db_Rollback()


    # read list
    @pytest.mark.parametrize(("device_type", "offset", "records"), [
        (None, None, None),
        (None, 100, 100),
        (None, 100000000, 1000),
        ('Nas', None, None),
        ('Nas', 100, 100),
        ('Nas', 100000000, 1000)])
    def Test_srv_db_Device_List(self, device_type, offset, records):
        self.db.srv_db_Device_List(device_type, offset, records)
        self.db.srv_db_Rollback()


    # insert record
    # def srv_db_Device_Insert(self, device_type, device_json):
#        self.db.srv_db_Rollback()


    # update record
    # def srv_db_Device_Update(self, guid, device_type, device_json):
#        self.db.srv_db_Rollback()


    # delete record
    # def srv_db_Device_Delete(self, guid):
#        self.db.srv_db_Rollback()


    # find detials by id
    # def srv_db_Device_Read(self, guid):
#        self.db.srv_db_Rollback()
