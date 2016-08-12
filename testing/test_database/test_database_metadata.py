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


class TestDatabaseMetadata(object):


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.srv_db_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.srv_db_Close()


    # read in the media with corresponding metadata
    @pytest.mark.parametrize(("media_guid"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630'),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633')])  # not found    
    def Test_srv_db_Read_Media_Metadata(self, media_guid):
        self.db.srv_db_Read_Media_Metadata(media_guid)
        self.db.srv_db_Rollback()


    # update record by tmdb
    # def srv_db_Metadata_Update(self, series_id_json, result_json, image_json):
#        self.db.srv_db_Rollback()


    # count all the generes
    def Test_srv_db_Metadata_Genre_List_Count(self):
        self.db.srv_db_Metadata_Genre_List_Count()
        self.db.srv_db_Rollback()


    # grab all the generes
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_srv_db_Metadata_Genre_List(self, offset, records):
        self.db.srv_db_Metadata_Genre_List(offset, records)
        self.db.srv_db_Rollback()


    # movie count by genre
    def Test_srv_db_Metadata_Movie_Count_By_Genre(self):
        self.db.srv_db_Metadata_Movie_Count_By_Genre()
        self.db.srv_db_Rollback()


    # metadata guid by imdb id
    @pytest.mark.parametrize(("uuid"), [
        ('tt0215948'),
        ('fakeid')])
    def Test_srv_db_Metadata_GUID_By_IMDB(self, uuid):
        self.db.srv_db_Metadata_GUID_By_IMDB(uuid)
        self.db.srv_db_Rollback()


    # metadata guid by tv id
    # def srv_db_Metadata_GUID_By_TVDB(self, thetvdb_uuid):
#        self.db.srv_db_Rollback()


    # see if metadata exists type and id
    @pytest.mark.parametrize(("uuid"), [
        ('71444'),
        ('fakeid')])
    def Test_srv_db_Metadata_GUID_By_TMDB(self, uuid):
        self.db.srv_db_Metadata_GUID_By_TMDB(uuid)
        self.db.srv_db_Rollback()


    # see if metadata exists type and id
    # def srv_db_Metadata_GUID_By_RT(self, rt_uuid):
#        self.db.srv_db_Rollback()


    # insert metadata from themoviedb
    # def srv_db_Metadata_Insert_TMDB(self, uuid_id, series_id, data_title, data_json, data_image_json):
#        self.db.srv_db_Rollback()


    # see if metadata exists via themovedbid
    @pytest.mark.parametrize(("uuid"), [
        ('71444'),
        ('fakeid')])
    def Test_srv_db_Metadata_TMDB_Count(self, uuid):
        self.db.srv_db_Metadata_TMDB_Count(uuid)
        self.db.srv_db_Rollback()


    # return list of movies
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_srv_db_Metadata_Movie_List(self, offset, records):
        self.db.srv_db_Metadata_Movie_List(offset, records)
        self.db.srv_db_Rollback()


    # grab the current metadata json id
    # def srv_db_Metadata_Fetch_Media_ID_Json(self, media_id_type, media_id_id, collection_media=False):
#        self.db.srv_db_Rollback()


    @pytest.mark.parametrize(("media_name", "media_year"), [
        ('Robocop', '1987'),
        ('Robocop', '2020'),
        ('FakeZZ', '2050')])
    def Test_srv_db_Find_Metadata_GUID(self, media_name, media_year):
        self.db.srv_db_Find_Metadata_GUID(media_name, media_year)
        self.db.srv_db_Rollback()


    # update the mediaid in metadata
    # def srv_db_Metadata_Update_Media_ID_From_Scudlee(self, media_tvid, media_imdbid, media_aniid):
#        self.db.srv_db_Rollback()
