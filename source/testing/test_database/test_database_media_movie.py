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


class TestDatabaseMediaMovie:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_media_random(self):
        """
        # find random movie
        """
        self.db_connection.db_rollback()
        self.db_connection.db_media_random()

    @pytest.mark.parametrize(("class_guid"), [
        ('928c56c3-253d-4e30-924e-5698be6d3d39'),  # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d30')])  # no exist
    def test_db_media_movie_count_by_genre(self, class_guid):
        """
        # movie count by genre
        """
        self.db_connection.db_rollback()
        self.db_connection.db_media_movie_count_by_genre(class_guid)

    @pytest.mark.parametrize(("class_guid", "list_type", "list_genre", "group_collection",
                              "include_remote"), [
                                 (
                                         '928c56c3-253d-4e30-924e-5698be6d3d39', None, 'All', False,
                                         False),
                                 # exists
                                 ('928c56c3-253d-4e30-924e-5698be6d3d39',
                                  None, 'All', False, True),
                                 # exists
                                 ('928c56c3-253d-4e30-924e-5698be6d3d39',
                                  None, 'All', True, True),
                                 # exists
                                 ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'Drama', False,
                                  False),  # exists
                                 ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'Drama', False,
                                  True),  # exists
                                 (
                                         '928c56c3-253d-4e30-924e-5698be6d3d39', None, 'Drama',
                                         True, True),
                                 # exists
                                 ('928c56c3-253d-4e30-924e-5698be6d3d30', None, 'All', False,
                                  False)])  # no exist
    def test_db_web_media_list_count(self, class_guid, list_type, list_genre,
                                     group_collection, include_remote):
        """
        # web media count
        """
        self.db_connection.db_rollback()
        self.db_connection.db_web_media_list_count(class_guid, list_type, list_genre,
                                                   group_collection, include_remote)

    @pytest.mark.parametrize(("class_guid", "list_type", "list_genre", "list_limit",
                              "group_collection", "offset", "include_remote"), [
                                 ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'All', 0, False, 0,
                                  False),  # exists
                                 ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'All', 0, False, 0,
                                  True),  # exists
                                 ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'All', 0, True, 0,
                                  True),  # exists
                                 (
                                         '928c56c3-253d-4e30-924e-5698be6d3d39', None, 'Drama', 0,
                                         False, 0,
                                         False),  # exists
                                 (
                                         '928c56c3-253d-4e30-924e-5698be6d3d39', None, 'Drama', 0,
                                         False, 0,
                                         True),  # exists
                                 ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'Drama', 0, True, 0,
                                  True),  # exists
                                 ('928c56c3-253d-4e30-924e-5698be6d3d30', None, 'All', 0, False, 0,
                                  False)])  # no exist
    def test_db_web_media_list(self, class_guid, list_type, list_genre,
                               list_limit, group_collection, offset, include_remote):
        """
        # web media return
        """
        self.db_connection.db_rollback()
        self.db_connection.db_web_media_list(class_guid, list_type, list_genre, list_limit,
                                             group_collection, offset, include_remote)
