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


class Test_database_media_movie:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # find random movie
    @pytest.mark.parametrize(("image_type"), [
        (True),
        (False)])
    def test_MK_Server_Database_Media_Random(self, image_type):
        self.db.MK_Server_Database_Media_Random(image_type)
        self.db.MK_Server_Database_Rollback()


    # movie count by genre
    @pytest.mark.parametrize(("class_guid"), [
        ('928c56c3-253d-4e30-924e-5698be6d3d39'),   # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d30')])  # no exist
    def test_MK_Server_Database_Media_Movie_Count_By_Genre(self, class_guid):
        self.db.MK_Server_Database_Media_Movie_Count_By_Genre(class_guid)
        self.db.MK_Server_Database_Rollback()


    # web media count
    @pytest.mark.parametrize(("class_guid", "list_type", "list_genre", "group_collection", "include_remote"), [
        ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'All', False, False),   # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'All', False, True),   # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'All', True, True),   # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'Drama', False, False),   # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'Drama', False, True),   # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'Drama', True, True),   # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d30', None, 'All', False, False)])  # no exist
    def test_MK_Server_Database_Web_Media_List_Count(self, class_guid, list_type, list_genre, group_collection, include_remote):
        self.db.MK_Server_Database_Web_Media_List_Count(class_guid, list_type, list_genre, group_collection, include_remote)
        self.db.MK_Server_Database_Rollback()


    # web media return
    @pytest.mark.parametrize(("class_guid", "list_type", "list_genre", "list_limit", "group_collection", "offset", "include_remote"), [
        ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'All', 0, False, 0, False),   # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'All', 0, False, 0, True),   # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'All', 0, True, 0, True),   # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'Drama', 0, False, 0, False),   # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'Drama', 0, False, 0, True),   # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d39', None, 'Drama', 0, True, 0, True),   # exists
        ('928c56c3-253d-4e30-924e-5698be6d3d30', None, 'All', 0, False, 0, False)])  # no exist
    def test_MK_Server_Database_Web_Media_List(self, class_guid, list_type, list_genre, list_limit, group_collection, offset, include_remote):
        self.db.MK_Server_Database_Web_Media_List(class_guid, list_type, list_genre, list_limit, group_collection, offset, include_remote)
        self.db.MK_Server_Database_Rollback()
