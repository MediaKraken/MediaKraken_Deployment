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


class Test_database_metadata_people:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # count person metadata
    def Test_MK_Server_Database_Metadata_Person_List_Count(self):
        self.db.MK_Server_Database_Metadata_Person_List_Count()
        self.db.MK_Server_Database_Rollback()


    # return list of people
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_MK_Server_Database_Metadata_Person_List(self, offset, records):
        self.db.MK_Server_Database_Metadata_Person_List(offset, records)
        self.db.MK_Server_Database_Rollback()


    # return person data
    # def MK_Server_Database_Metadata_Person_By_GUID(self, guid):
#         self.db.MK_Server_Database_Rollback()


    # return person data by name
    # def MK_Server_Database_Metadata_Person_By_Name(self, person_name):
#         self.db.MK_Server_Database_Rollback()


    # does person exist already by host/id
    # def MK_Server_Database_Metadata_Person_ID_Count(self, host_type, guid):
#         self.db.MK_Server_Database_Rollback()


    # insert person
    # def MK_Server_Database_Metdata_Person_Insert(self, person_name, media_id_json, person_json, image_json=None):
#         self.db.MK_Server_Database_Rollback()


    # batch insert from json of crew/cast
    # def MK_Server_Database_Metadata_Person_Insert_Cast_Crew(self, meta_type, person_json):
#         self.db.MK_Server_Database_Rollback()


    # find other media for person
    # def MK_Server_Database_Metadata_Person_As_Seen_In(self, person_guid):
#         self.db.MK_Server_Database_Rollback()
