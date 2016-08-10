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
sys.path.append("../common")
sys.path.append("../server") # for db import
import database as database_base


class Test_database_tv_schedule:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # read the stations
    def test_MK_Server_Database_TV_Stations_Read(self):
        self.db.MK_Server_Database_TV_Stations_Read()
        self.db.MK_Server_Database_Rollback()


    # read the stationid list
    def test_MK_Server_Database_TV_Stations_Read_StationID_List(self):
        self.db.MK_Server_Database_TV_Stations_Read_StationID_List()
        self.db.MK_Server_Database_Rollback()


    # insert station/channel unless it exists
    # def MK_Server_Database_TV_Station_Insert(self, station_id, channel_id):
#        self.db.MK_Server_Database_Rollback()


    # channel exist check
    # def MK_Server_Database_TV_Station_Exist(self, station_id, channel_id):
 #       self.db.MK_Server_Database_Rollback()


    # update station/channel info
    # def MK_Server_Database_TV_Station_Update(self, station_name, station_id, station_json):
  #      self.db.MK_Server_Database_Rollback()


    # insert schedule info
    # def MK_Server_Database_TV_Schedule_Insert(self, station_id, schedule_date, schedule_json):
   #     self.db.MK_Server_Database_Rollback()


    # insert program info
    # def MK_Server_Database_TV_Program_Insert(self, program_id, program_json):
    #    self.db.MK_Server_Database_Rollback()


    # tv shows for schedule display
    # def MK_Server_Database_TV_Schedule_By_Date(self, display_date):
     #   self.db.MK_Server_Database_Rollback()
