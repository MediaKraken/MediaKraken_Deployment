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


class Test_database_usage:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    def Test_MK_Server_Database_Usage_Top10_AllTime(self):
        self.db.MK_Server_Database_Usage_Top10_AllTime()
        self.db.MK_Server_Database_Rollback()


    def Test_MK_Server_Database_Usage_Top10_Movie(self):
        self.db.MK_Server_Database_Usage_Top10_Movie()
        self.db.MK_Server_Database_Rollback()


    def Test_MK_Server_Database_Usage_Top10_TV_Show(self):
        self.db.MK_Server_Database_Usage_Top10_TV_Show()
        self.db.MK_Server_Database_Rollback()


    def Test_MK_Server_Database_Usage_Top10_TV_Episode(self):
        self.db.MK_Server_Database_Usage_Top10_TV_Episode()
        self.db.MK_Server_Database_Rollback()
