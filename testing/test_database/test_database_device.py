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


import pytest
import sys
sys.path.append("../MediaKraken_Common")
sys.path.append("../MediaKraken_Server")  # for db import
import database as database_base


class Test_database_devices:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # count device
    def test_MK_Server_Database_Device_Count(self):
        self.db.MK_Server_Database_Device_Count()
        self.db.MK_Server_Database_Rollback()


    # read list
    @pytest.mark.parametrize(("device_type", "offset", "records"), [
        (None, None, None),
        (None, 100, 100),
        (None, 100000000, 1000),
        ('Nas', None, None),
        ('Nas', 100, 100),
        ('Nas', 100000000, 1000)])
    def test_MK_Server_Database_Device_List(self, device_type, offset, records):
        self.db.MK_Server_Database_Device_List(device_type, offset, records)
        self.db.MK_Server_Database_Rollback()


    # insert record
    # def MK_Server_Database_Device_Insert(self, device_type, device_json):
#        self.db.MK_Server_Database_Rollback()


    # update record
    # def MK_Server_Database_Device_Update(self, guid, device_type, device_json):
#        self.db.MK_Server_Database_Rollback()


    # delete record
    # def MK_Server_Database_Device_Delete(self, guid):
#        self.db.MK_Server_Database_Rollback()


    # find detials by id
    # def MK_Server_Database_Device_Read(self, guid):
#        self.db.MK_Server_Database_Rollback()
