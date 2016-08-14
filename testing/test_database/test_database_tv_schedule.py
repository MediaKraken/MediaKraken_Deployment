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


class TestDatabaseTVSchedule(object):


    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.srv_db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db_connection.srv_db_close()


    # read the stations
    def test_srv_db_tv_stations_read(self):
        self.db_connection.srv_db_tv_stations_read()
        self.db_connection.srv_db_rollback()


    # read the stationid list
    def test_srv_db_tv_stations_read_StationID_List(self):
        self.db_connection.srv_db_tv_stations_read_StationID_List()
        self.db_connection.srv_db_rollback()


    # insert station/channel unless it exists
    # def srv_db_tv_station_insert(self, station_id, channel_id):
#        self.db_connection.srv_db_rollback()


    # channel exist check
    # def srv_db_tv_station_exist(self, station_id, channel_id):
 #       self.db_connection.srv_db_rollback()


    # update station/channel info
    # def srv_db_tv_station_update(self, station_name, station_id, station_json):
  #      self.db_connection.srv_db_rollback()


    # insert schedule info
    # def srv_db_tv_schedule_insert(self, station_id, schedule_date, schedule_json):
   #     self.db_connection.srv_db_rollback()


    # insert program info
    # def srv_db_tv_program_insert(self, program_id, program_json):
    #    self.db_connection.srv_db_rollback()


    # tv shows for schedule display
    # def srv_db_tv_schedule_by_date(self, display_date):
     #   self.db_connection.srv_db_rollback()
