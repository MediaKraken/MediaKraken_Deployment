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

import json
import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
import database as database_base


class TestDatabaseTVSchedule:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_tv_stations_read(self):
        """
        # read the stations
        """
        self.db_connection.db_rollback()
        self.db_connection.db_tv_stations_read()

    def test_db_tv_stations_read_stationid_list(self):
        """
        # read the stationid list
        """
        self.db_connection.db_rollback()
        self.db_connection.db_tv_stations_read_stationid_list()

    # insert station/channel unless it exists
    # def db_tv_station_insert(self, station_id, channel_id):
    #        self.db_connection.db_rollback()

    # channel exist check
    # def db_tv_station_exist(self, station_id, channel_id):
    #       self.db_connection.db_rollback()

    # update station/channel info
    # def db_tv_station_update(self, station_name, station_id, station_json):
    #      self.db_connection.db_rollback()

    # insert schedule info
    # def db_tv_schedule_insert(self, station_id, schedule_date, schedule_json):
    #     self.db_connection.db_rollback()

    @pytest.mark.parametrize(("program_id", "program_json"), [
        ('100', json.dumps({'program': 'stuff'})),
        ('100', json.dumps({'program': 'stuff update'}))])  # to test update
    def test_db_tv_program_insert(self, program_id, program_json):
        """
        # insert program info
        """
        self.db_connection.db_rollback()
        self.db_connection.db_tv_program_insert(program_id, program_json)

    @pytest.mark.parametrize(("display_date"), [
        ('20160820'),
        ('19700501')])
    def test_db_tv_schedule_by_date(self, display_date):
        """
        # tv shows for schedule display
        """
        self.db_connection.db_rollback()
        self.db_connection.db_tv_schedule_by_date(display_date)
