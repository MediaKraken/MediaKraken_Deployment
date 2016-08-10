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
sys.path.append("../MediaKraken_Common")
sys.path.append("../MediaKraken_Server")  # for db import
import database as database_base


class Test_database_collection:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # find all known media
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100,100),
        (100000000,1000)])
    def test_MK_Server_Database_Collection_List(self, offset, records):
        self.db.MK_Server_Database_Collection_List(offset, records)
        self.db.MK_Server_Database_Rollback()


    # read collection data from json metadata
    def test_MK_Server_Database_Media_Collection_Scan(self):
        self.db.MK_Server_Database_Media_Collection_Scan()
        self.db.MK_Server_Database_Rollback()


    # find guid of collection name
    @pytest.mark.parametrize(("collection_name"), [
        ('Darko Collection'),
        ('fakecollectionstuff')])
    def test_MK_Server_Database_Collection_GUID_By_Name(self, collection_name):
        self.db.MK_Server_Database_Collection_GUID_By_Name(collection_name)
        self.db.MK_Server_Database_Rollback()


    # find guid of collection name
    # def MK_Server_Database_Collection_By_TMDB(self, tmdb_id):
#        self.db.MK_Server_Database_Rollback()


    # insert collection
    # def MK_Server_Database_Collection_Insert(self, collection_name, guid_json, metadata_json, localimage_json):
#        self.db.MK_Server_Database_Rollback()


    # update collection ids
    # def MK_Server_Database_Collection_Update(self, collection_guid, guid_json):
#        self.db.MK_Server_Database_Rollback()


    # pull in colleciton info
    # def MK_Server_Database_Collection_Read_By_GUID(self, media_uuid):
#        self.db.MK_Server_Database_Rollback()
