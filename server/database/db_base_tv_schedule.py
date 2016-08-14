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


def srv_db_tv_stations_read(self):
    """
    # read the stations
    """
    self.sql3_cursor.execute('select mm_tv_stations_id,mm_tv_station_name,mv_tv_station_id,'\
        'mv_tv_station_channel from mm_tv_stations')
    return self.sql3_cursor.fetchall()


def srv_db_tv_stations_read_stationid_list(self):
    """
    # read the stationid list
    """
    self.sql3_cursor.execute('select mv_tv_station_id from mm_tv_stations')
    return self.sql3_cursor.fetchall()


def srv_db_tv_station_insert(self, station_id, channel_id):
    """
    # insert station/channel unless it exists
    """
    if self.srv_db_tv_station_exist(station_id, channel_id) == 0:
        self.sql3_cursor.execute('insert into mm_tv_stations (mm_tv_stations_id, mv_tv_station_id,'\
            ' mv_tv_station_channel) values (%s, %s, %s)',\
            (str(uuid.uuid4()), station_id, channel_id))


def srv_db_tv_station_exist(self, station_id, channel_id):
    """
    # channel exist check
    """
    self.sql3_cursor.execute('select count(*) from mm_tv_stations where mv_tv_station_id = %s'\
        ' and mv_tv_station_channel = %s', (station_id, channel_id))
    return self.sql3_cursor.fetchone()[0]


def srv_db_tv_station_update(self, station_name, station_id, station_json):
    """
    # update station/channel info
    """
    self.sql3_cursor.execute('update mm_tv_stations set mm_tv_station_name = %s,'\
        ' mv_tv_station_json = %s where mv_tv_station_id = %s',\
        (station_name, station_json, station_id))


def srv_db_tv_schedule_insert(self, station_id, schedule_date, schedule_json):
    """
    # insert schedule info
    """
    self.sql3_cursor.execute('select count(*) from mm_tv_schedule'\
        ' where mm_tv_schedule_station_id = %s and mm_tv_schedule_date = %s',\
        (station_id, schedule_date))
    if self.sql3_cursor.fetchone()[0] > 0:
        self.sql3_cursor.execute('update mm_tv_schedule set mm_tv_schedule_json = %s'\
            ' where mm_tv_schedule_station_id = %s and mm_tv_schedule_date = %s',\
            (schedule_json, station_id, schedule_date))
    else:
        self.sql3_cursor.execute('insert into mm_tv_schedule (mm_tv_schedule_id,'\
            ' mm_tv_schedule_station_id, mm_tv_schedule_date, mm_tv_schedule_json)'\
            ' values (%s, %s, %s, %s)',\
            (str(uuid.uuid4()), station_id, schedule_date, schedule_json))


def srv_db_tv_program_insert(self, program_id, program_json):
    """
    # insert program info
    """
    self.sql3_cursor.execute('select count(*) from mm_tv_schedule_program'\
        ' where mm_tv_schedule_program_id = %s', (program_id,))
    if self.sql3_cursor.fetchone()[0] > 0:
        self.sql3_cursor.execute('update mm_tv_schedule_program'\
            ' set mm_tv_schedule_program_json = %s where mm_tv_schedule_program_id = %s',\
            (program_json, program_id))
    else:
        self.sql3_cursor.execute('insert into mm_tv_schedule_program'\
            ' (mm_tv_schedule_program_guid, mm_tv_schedule_program_id,'\
            ' mm_tv_schedule_program_json) values (%s, %s, %s)',\
            (str(uuid.uuid4()), program_id, program_json))


def srv_db_tv_schedule_by_date(self, display_date):
    """
    # tv shows for schedule display
    """
    self.sql3_cursor.execute('select mm_tv_station_name, mv_tv_station_channel,'\
        ' mm_tv_schedule_json from mm_tv_stations, mm_tv_schedule'\
        ' where mm_tv_schedule_station_id = mv_tv_station_id and mm_tv_schedule_date = %s'\
        ' order by mm_tv_station_name, mm_tv_schedule_json->\'airDateTime\'', (display_date,))
    return self.sql3_cursor.fetchall()
