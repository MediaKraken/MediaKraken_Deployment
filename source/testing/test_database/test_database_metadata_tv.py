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


class TestDatabaseMetadataTV:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    # metadata guid by name
    # def db_metatv_guid_by_tvshow_name(self, tvshow_name, tvshow_year=None):
    #        self.db_connection.db_rollback()

    # metadata guid by imdb id
    # def db_metaTV_guid_by_imdb(self, imdb_uuid):
    #        self.db_connection.db_rollback()

    # metadata guid by tv id
    # def db_metatv_guid_by_tvdb(self, thetvdb_uuid):
    #        self.db_connection.db_rollback()

    # metadata guid by tvmaze id
    # def db_metaTV_guid_by_tvmaze(self, tvmaze_uuid):
    #        self.db_connection.db_rollback()

    def test_db_meta_tvshow_list_count(self):
        """
        # tvshow count
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_tvshow_list_count()

    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_meta_tvshow_list(self, offset, records):
        """
        # return list of tvshows
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_tvshow_list(offset, records)

    # update image json
    # def db_meta_tvshow_update_image(self, image_json, metadata_uuid):
#        self.db_connection.db_rollback()


# fetch tvmaze rows to update
# def db_meta_tvshow_images_to_update(self, image_type):
#        self.db_connection.db_rollback()
#

# return metadata for tvshow
# def db_meta_tvshow_detail(self, guid):
#        self.db_connection.db_rollback()


# read in the tv episodes metadata by guid
# def db_read_tvmeta_episodes(self, show_guid):
#        self.db_connection.db_rollback()


# grab tvmaze ep data for eps per season
# def db_read_tvmeta_eps_season(self, show_guid):
#        self.db_connection.db_rollback()


# grab episodes within the season
# def db_read_tvmeta_season_eps_list(self, show_guid, season_number):
#        self.db_connection.db_rollback()


# grab episode detail
# def db_read_tvmeta_episode(self, show_guid, season_number, episode_number):
#        self.db_connection.db_rollback()
