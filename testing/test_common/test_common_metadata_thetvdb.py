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
from MK_Common_Metadata_TheTVDB import *


class TestCommonMetadataTheTVDB(object):


    @classmethod
    def setup_class(self):
        self.db = MK_Common_Metadata_TheTVDB.MK_Common_Metadata_TheTVDB_API()


    @classmethod
    def teardown_class(self):
        pass


# def MK_Common_Metadata_TheTVDB_Updates(self, frequency='day'):


# def MK_Common_Metadata_TheTVDB_Get_ZIP_By_ID(self, tv_show_id, lang_code='en'):


    def Test_MK_Common_Metadata_TheTVDB_Get_Server_Epoc_Time(self):
        MK_Common_Metadata_TheTVDB_Get_Server_Epoc_Time()


# def MK_Common_Metadata_TheTVDB_Updates_By_Epoc(self, epoc_timestamp):


# def MK_Common_Metadata_TheTVDB_Update_Series_Read(self, tv_show_id, lang_code = 'en'):


# def MK_Common_Metadata_TheTVDB_Update_Episode_Read(self, tv_eps_id, lang_code = 'en'):
