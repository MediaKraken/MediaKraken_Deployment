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

sys.path.append('.')
import database as database_base


class TestDatabaseUsage:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_usage_top10_alltime(self):
        """
        top 10 alltime
        """
        self.db_connection.db_rollback()
        self.db_connection.db_usage_top10_alltime()

    def test_db_usage_top10_movie(self):
        """
        top 10 movie
        """
        self.db_connection.db_rollback()
        self.db_connection.db_usage_top10_movie()

    def test_db_usage_top10_tv_show(self):
        """
        top 10 tv show
        """
        self.db_connection.db_rollback()
        self.db_connection.db_usage_top10_tv_show()

    def test_db_usage_top10_tv_episode(self):
        """
        top 10 tv episode
        """
        self.db_connection.db_rollback()
        self.db_connection.db_usage_top10_tv_episode()
