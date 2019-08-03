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

import sys

sys.path.append('.')
from common import common_schedules_direct


class TestCommonSchedulesDirect:

    @classmethod
    def setup_class(self):
        self.sd_connection = common_schedules_direct.CommonSchedulesDirect()

    @classmethod
    def teardown_class(self):
        pass

    #    def com_Schedules_Direct_Login(self, user_name, user_password):

    def test_com_schedules_direct_status(self):
        """
        Test function
        """
        self.sd_connection.com_schedules_direct_status()

    def test_com_schedules_direct_client_version(self):
        """
        Test function
        """
        self.sd_connection.com_schedules_direct_client_version()

    #    def com_Schedules_Direct_Available(self, countries=None):

    #    def com_Schedules_Direct_Headends(self, country_code, postal_code):

    #    def com_Schedules_Direct_Lineup_Add(self, lineup_id):

    def test_com_schedules_direct_lineup_list(self):
        """
        Test function
        """
        self.sd_connection.com_schedules_direct_lineup_list()

#    def com_Schedules_Direct_Lineup_Delete(self, lineup_id):


#    def com_Schedules_Direct_Lineup_Channel_Map(self, lineup_id):


#    def com_Schedules_Direct_Program_Info(self, program_ids):


# this one is only for EP types, not MV
#    def com_Schedules_Direct_Program_Desc(self, program_ids):


#    def com_Schedules_Direct_Schedules_by_StationID(self, station_ids):


#    def com_Schedules_Direct_MD5(self, station_ids):


#    def com_Schedules_Still_Running(self, program_id):


#    def com_Schedules_Program_Metadata(self, program_ids):
