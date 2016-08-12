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
sys.path.append("../common")
from MK_Common_Schedules_Direct import *


class test_MK_Common_Schedules_Direct_API:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_Schedules_Direct.MK_Common_Schedules_Direct_API()


    @classmethod
    def teardown_class(self):
        pass


#    def MK_Common_Schedules_Direct_Login(self, user_name, user_password):


    def test_MK_Common_Schedules_Direct_Status(self):
        MK_Common_Schedules_Direct_Status()


    def test_MK_Common_Schedules_Direct_Client_Version(self):
        MK_Common_Schedules_Direct_Client_Version()


#    def MK_Common_Schedules_Direct_Available(self, countries=None):


#    def MK_Common_Schedules_Direct_Headends(self, country_code, postal_code):


#    def MK_Common_Schedules_Direct_Lineup_Add(self, lineup_id):


    def test_MK_Common_Schedules_Direct_Lineup_List(self):
        MK_Common_Schedules_Direct_Lineup_List()


#    def MK_Common_Schedules_Direct_Lineup_Delete(self, lineup_id):


#    def MK_Common_Schedules_Direct_Lineup_Channel_Map(self, lineup_id):


#    def MK_Common_Schedules_Direct_Program_Info(self, program_ids):


    # this one is only for EP types, not MV
#    def MK_Common_Schedules_Direct_Program_Desc(self, program_ids):


#    def MK_Common_Schedules_Direct_Schedules_By_StationID(self, station_ids):


#    def MK_Common_Schedules_Direct_MD5(self, station_ids):


#    def MK_Common_Schedules_Still_Running(self, program_id):


#    def MK_Common_Schedules_Program_Metadata(self, program_ids):
