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


class Test_database_metadata_tv:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # metadata guid by name
    # def MK_Server_Database_MetadataTV_GUID_By_TVShow_Name(self, tvshow_name, tvshow_year=None):
#        self.db.MK_Server_Database_Rollback()


    # metadata guid by imdb id
    # def MK_Server_Database_MetadataTV_GUID_By_IMDB(self, imdb_uuid):
#        self.db.MK_Server_Database_Rollback()


    # metadata guid by tv id
    # def MK_Server_Database_MetadataTV_GUID_By_TVDB(self, thetvdb_uuid):
#        self.db.MK_Server_Database_Rollback()


    # metadata guid by tvmaze id
    # def MK_Server_Database_MetadataTV_GUID_By_TVMaze(self, tvmaze_uuid):
#        self.db.MK_Server_Database_Rollback()


    # metadata guid by tvrage id
    # def MK_Server_Database_MetadataTV_GUID_By_TVRage(self, tvrage_uuid):
#        self.db.MK_Server_Database_Rollback()


    # tvshow count
    def test_MK_Server_Database_Metadata_TVShow_List_Count(self):
        self.db.MK_Server_Database_Metadata_TVShow_List_Count()
        self.db.MK_Server_Database_Rollback()


    # return list of tvshows
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100,100),
        (100000000,1000)])
    def test_MK_Server_Database_Metadata_TVShow_List(self, offset, records):
        self.db.MK_Server_Database_Metadata_TVShow_List(offset, records)
        self.db.MK_Server_Database_Rollback()


    # update image json
    # def MK_Server_Database_Metadata_TVShow_Update_Image(self, image_json, metadata_uuid):
#        self.db.MK_Server_Database_Rollback()


    # fetch tvmaze rows to update
    # def MK_Server_Database_Metadata_TVShow_Images_To_Update(self, image_type):
#        self.db.MK_Server_Database_Rollback()
#

    # return metadata for tvshow
    # def MK_Server_Database_Metadata_TVShow_Detail(self, guid):
#        self.db.MK_Server_Database_Rollback()


    # read in the tv episodes metadata by guid
    # def MK_Server_Database_Read_TVMetadata_Episodes(self, show_guid):
#        self.db.MK_Server_Database_Rollback()


    # grab tvmaze ep data for eps per season
    # def MK_Server_Database_Read_TVMetadata_Eps_Season(self, show_guid):
#        self.db.MK_Server_Database_Rollback()


    # grab episodes within the season
    # def MK_Server_Database_Read_TVMetadata_Season_Eps_List(self, show_guid, season_number):
#        self.db.MK_Server_Database_Rollback()


    # grab episode detail
    # def MK_Server_Database_Read_TVMetadata_Episode(self, show_guid, season_number, episode_number):
#        self.db.MK_Server_Database_Rollback()
