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

import pytest  # pylint: disable=W0611

sys.path.append('.')
import database as database_base


class TestDatabaseMetadata:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    @pytest.mark.parametrize(("media_guid"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630'),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633')])  # not found
    def test_db_read_media_metadata(self, media_guid):
        """
        # read in the media with corresponding metadata
        """
        self.db_connection.db_rollback()
        self.db_connection.db_read_media_metadata(media_guid)

    # update record by tmdb
    # def db_meta_update(self, series_id_json, result_json, image_json):
    #        self.db_connection.db_rollback()

    def test_db_meta_genre_list_count(self):
        """
        # count all the generes
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_genre_list_count()

    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_meta_genre_list(self, offset, records):
        """
        # grab all the generes
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_genre_list(offset, records)

    def test_db_meta_movie_count_genre(self):
        """
        # movie count by genre
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_movie_count_genre()

    @pytest.mark.parametrize(("uuid"), [
        ('tt0215948'),
        ('fakeid')])
    def test_db_meta_guid_by_imdb(self, uuid):
        """
        # metadata guid by imdb id
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_guid_by_imdb(uuid)

    # metadata guid by tv id
    # def db_meta_guid_by_tvdb(self, thetvdb_uuid):
    #        self.db_connection.db_rollback()

    @pytest.mark.parametrize(("uuid"), [
        ('71444'),
        ('fakeid')])
    def test_db_meta_guid_by_tmdb(self, uuid):
        """
        # see if metadata exists type and id
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_guid_by_tmdb(uuid)

    # see if metadata exists type and id
    # def db_meta_guid_by_rt(self, rt_uuid):
    #        self.db_connection.db_rollback()

    # insert metadata from themoviedb
    # def db_meta_insert_tmdb(self, uuid_id, series_id, data_title, data_json, data_image_json):
    #        self.db_connection.db_rollback()

    @pytest.mark.parametrize(("uuid"), [
        ('71444'),
        ('fakeid')])
    def test_db_meta_tmdb_count(self, uuid):
        """
        # see if metadata exists via themovedbid
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_tmdb_count(uuid)

    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_meta_movie_list(self, offset, records):
        """
        # return list of movies
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_movie_list(offset, records)

    # grab the current metadata json id
    # def db_meta_fetch_media_id_json(self, media_id_type, media_id_id, collection_media=False):
    #        self.db_connection.db_rollback()

    @pytest.mark.parametrize(("media_name", "media_year"), [
        ('Robocop', '1987'),
        ('Robocop', '2020'),
        ('FakeZZ', '2050')])
    def test_db_find_metadata_guid(self, media_name, media_year):
        """
        Test function
        """
        self.db_connection.db_rollback()
        self.db_connection.db_find_metadata_guid(media_name, media_year)

    # update the mediaid in metadata
    # def db_meta_update_media_id_from_scudlee(self, media_tvid, media_imdbid, media_aniid):
#        self.db_connection.db_rollback()
