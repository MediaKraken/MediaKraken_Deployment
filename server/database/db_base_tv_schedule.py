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
import logging
import uuid


# read the stations
def MK_Server_Database_TV_Stations_Read(self):
    self.sql3_cursor.execute(u'select mm_tv_stations_id,mm_tv_station_name,mv_tv_station_id,mv_tv_station_channel from mm_tv_stations')
    return self.sql3_cursor.fetchall()


# read the stationid list
def MK_Server_Database_TV_Stations_Read_StationID_List(self):
    self.sql3_cursor.execute(u'select mv_tv_station_id from mm_tv_stations')
    return self.sql3_cursor.fetchall()


# insert station/channel unless it exists
def MK_Server_Database_TV_Station_Insert(self, station_id, channel_id):
    if self.MK_Server_Database_TV_Station_Exist(station_id, channel_id) == 0:
        self.sql3_cursor.execute(u'insert into mm_tv_stations (mm_tv_stations_id, mv_tv_station_id, mv_tv_station_channel) values (%s, %s, %s)', (str(uuid.uuid4()), station_id, channel_id))


# channel exist check
def MK_Server_Database_TV_Station_Exist(self, station_id, channel_id):
    self.sql3_cursor.execute(u'select count(*) from mm_tv_stations where mv_tv_station_id = %s and mv_tv_station_channel = %s', (station_id, channel_id))
    return self.sql3_cursor.fetchone()[0]


# update station/channel info
def MK_Server_Database_TV_Station_Update(self, station_name, station_id, station_json):
    self.sql3_cursor.execute(u'update mm_tv_stations set mm_tv_station_name = %s, mv_tv_station_json = %s where mv_tv_station_id = %s', (station_name, station_json, station_id))


# insert schedule info
def MK_Server_Database_TV_Schedule_Insert(self, station_id, schedule_date, schedule_json):
    self.sql3_cursor.execute(u'select count(*) from mm_tv_schedule where mm_tv_schedule_station_id = %s and mm_tv_schedule_date = %s', (station_id, schedule_date))
    if self.sql3_cursor.fetchone()[0] > 0:
        self.sql3_cursor.execute(u'update mm_tv_schedule set mm_tv_schedule_json = %s where mm_tv_schedule_station_id = %s and mm_tv_schedule_date = %s', (schedule_json, station_id, schedule_date))
    else:
        self.sql3_cursor.execute(u'insert into mm_tv_schedule (mm_tv_schedule_id, mm_tv_schedule_station_id, mm_tv_schedule_date, mm_tv_schedule_json) values (%s, %s, %s, %s)', (str(uuid.uuid4()), station_id, schedule_date, schedule_json))


# insert program info
def MK_Server_Database_TV_Program_Insert(self, program_id, program_json):
    self.sql3_cursor.execute(u'select count(*) from mm_tv_schedule_program where mm_tv_schedule_program_id = %s', (program_id,))
    if self.sql3_cursor.fetchone()[0] > 0:
        self.sql3_cursor.execute(u'update mm_tv_schedule_program set mm_tv_schedule_program_json = %s where mm_tv_schedule_program_id = %s', (program_json, program_id))
    else:
        self.sql3_cursor.execute(u'insert into mm_tv_schedule_program (mm_tv_schedule_program_guid, mm_tv_schedule_program_id, mm_tv_schedule_program_json) values (%s, %s, %s)', (str(uuid.uuid4()), program_id, program_json))


# tv shows for schedule display
def MK_Server_Database_TV_Schedule_By_Date(self, display_date):
    self.sql3_cursor.execute(u'select mm_tv_station_name, mv_tv_station_channel, mm_tv_schedule_json from mm_tv_stations, mm_tv_schedule where mm_tv_schedule_station_id = mv_tv_station_id and mm_tv_schedule_date = %s order by mm_tv_station_name, mm_tv_schedule_json->\'airDateTime\'', (display_date,))
    return self.sql3_cursor.fetchall()
