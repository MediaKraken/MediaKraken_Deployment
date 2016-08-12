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


class TestDatabaseMetadataTVMaze(object):


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.srv_db_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.srv_db_Close()


    # metadata changed date by uuid
    # def srv_db_MetadataTVMaze_Changed_UUID(self, maze_uuid):
#        self.db.srv_db_Rollback()


    # insert
    # def srv_db_MetadataTVMaze_Insert(self, series_id_json, tvmaze_name, show_detail, image_json):
#         self.db.srv_db_Rollback()


    # updated
    # def srv_db_MetadataTVMaze_Update(self, series_id_json, tvmaze_name, show_detail, tvmaze_id):
#         self.db.srv_db_Rollback()
