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


def srv_db_usage_top10_alltime(self):
    """
    Top 10 of all time
    """
    self.sql3_cursor.execute('select blah from blah order by blah limit 10')
    return self.sql3_cursor.fetchall()


def srv_db_usage_top10_movie(self):
    """
    Top 10 movies
    """
    self.sql3_cursor.execute('select mm_metadata_user_json->\'Watched\'->\'Times\''\
        ' from mm_metadata_movie order by mm_metadata_user_json->\'Watched\'->\'Times\''\
        ' desc limit 10')
    return self.sql3_cursor.fetchall()


def srv_db_usage_top10_tv_show(self):
    """
    Top 10 TV show
    """
    self.sql3_cursor.execute('select mm_metadata_tvshow_user_json ->\'Watched\'->\'Times\''\
        ' from mm_metadata_tvshow order by mm_metadata_tvshow_user_json ->\'Watched\'->\'Times\''\
        ' desc limit 10')
    return self.sql3_cursor.fetchall()


def srv_db_usage_top10_tv_episode(self):
    """
    Top 10 TV episode
    """
    self.sql3_cursor.execute('select blah from blah order by blah limit 10')
    return self.sql3_cursor.fetchall()
