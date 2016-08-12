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


class TestDatabaseMetadataTV(object):


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.srv_db_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.srv_db_Close()


    # metadata guid by name
    # def srv_db_MetadataTV_GUID_By_TVShow_Name(self, tvshow_name, tvshow_year=None):
#        self.db.srv_db_Rollback()


    # metadata guid by imdb id
    # def srv_db_MetadataTV_GUID_By_IMDB(self, imdb_uuid):
#        self.db.srv_db_Rollback()


    # metadata guid by tv id
    # def srv_db_MetadataTV_GUID_By_TVDB(self, thetvdb_uuid):
#        self.db.srv_db_Rollback()


    # metadata guid by tvmaze id
    # def srv_db_MetadataTV_GUID_By_TVMaze(self, tvmaze_uuid):
#        self.db.srv_db_Rollback()


    # metadata guid by tvrage id
    # def srv_db_MetadataTV_GUID_By_TVRage(self, tvrage_uuid):
#        self.db.srv_db_Rollback()


    # tvshow count
    def Test_srv_db_Metadata_TVShow_List_Count(self):
        self.db.srv_db_Metadata_TVShow_List_Count()
        self.db.srv_db_Rollback()


    # return list of tvshows
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_srv_db_Metadata_TVShow_List(self, offset, records):
        self.db.srv_db_Metadata_TVShow_List(offset, records)
        self.db.srv_db_Rollback()


    # update image json
    # def srv_db_Metadata_TVShow_Update_Image(self, image_json, metadata_uuid):
#        self.db.srv_db_Rollback()


    # fetch tvmaze rows to update
    # def srv_db_Metadata_TVShow_Images_To_Update(self, image_type):
#        self.db.srv_db_Rollback()
#

    # return metadata for tvshow
    # def srv_db_Metadata_TVShow_Detail(self, guid):
#        self.db.srv_db_Rollback()


    # read in the tv episodes metadata by guid
    # def srv_db_Read_TVMetadata_Episodes(self, show_guid):
#        self.db.srv_db_Rollback()


    # grab tvmaze ep data for eps per season
    # def srv_db_Read_TVMetadata_Eps_Season(self, show_guid):
#        self.db.srv_db_Rollback()


    # grab episodes within the season
    # def srv_db_Read_TVMetadata_Season_Eps_List(self, show_guid, season_number):
#        self.db.srv_db_Rollback()


    # grab episode detail
    # def srv_db_Read_TVMetadata_Episode(self, show_guid, season_number, episode_number):
#        self.db.srv_db_Rollback()
