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


class TestDatabaseiradio(object):


    @classmethod
    def setup_class(self):
        self.db = database_base.MKServerDatabase()
        self.db.srv_db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.srv_db_close()


    # insert iradio channel
    # def srv_db_iRadio_Insert(self, radio_channel):
#        self.db.srv_db_rollback()


    # iradio count
    @pytest.mark.parametrize(("active_station"), [
        (True,),
        (False)])
    def Test_srv_db_iRadio_List_Count(self, active_station):
        self.db.srv_db_iRadio_List_Count(active_station)
        self.db.srv_db_rollback()


    # iradio list
    @pytest.mark.parametrize(("active_station", "offset", "records"), [
        (True, None, None),
        (True, 100, 100),
        (True, 100000000, 1000),
        (False, None, None),
        (False, 100, 100),
        (False, 100000000, 1000)])
    def Test_srv_db_iRadio_List(self, active_station, offset, records):
        self.db.srv_db_iRadio_List(active_station, offset, records)
        self.db.srv_db_rollback()
