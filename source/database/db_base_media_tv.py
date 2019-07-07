'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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


def db_web_tvmedia_list(self, genre_type=None, list_limit=None,
                        group_collection=False, offset=0, search_value=None):
    """
    # grab tv data
    """
    if search_value is not None:
        self.db_cursor.execute('select mm_metadata_tvshow_name, mm_metadata_tvshow_guid,'
                               ' count(*) as mm_count, COALESCE(mm_metadata_tvshow_localimage_json'
                               '->\'Images\'->\'tvmaze\'->>\'Poster\','
                               ' mm_metadata_tvshow_localimage_json'
                               '->\'Images\'->\'thetvdb\'->>\'Poster\') from mm_metadata_tvshow,'
                               ' mm_media where mm_media_metadata_guid = mm_metadata_tvshow_guid'
                               ' and mm_metadata_tvshow_name %% %s'
                               ' group by mm_metadata_tvshow_guid'
                               ' order by LOWER(mm_metadata_tvshow_name)'
                               ' offset %s limit %s', (search_value, offset, list_limit))
    else:
        self.db_cursor.execute('select mm_metadata_tvshow_name, mm_metadata_tvshow_guid,'
                               ' count(*) as mm_count, COALESCE(mm_metadata_tvshow_localimage_json'
                               '->\'Images\'->\'tvmaze\'->>\'Poster\','
                               ' mm_metadata_tvshow_localimage_json'
                               '->\'Images\'->\'thetvdb\'->>\'Poster\') from mm_metadata_tvshow,'
                               ' mm_media where mm_media_metadata_guid = mm_metadata_tvshow_guid'
                               ' group by mm_metadata_tvshow_guid'
                               ' order by LOWER(mm_metadata_tvshow_name)'
                               ' offset %s limit %s', (offset, list_limit))
    return self.db_cursor.fetchall()


def db_web_tvmedia_list_count(self, genre_type=None, group_collection=False, search_value=None):
    """
    # grab tv data count
    """
    self.db_cursor.execute('select count(*) from mm_metadata_tvshow, mm_media'
                           ' where mm_media_metadata_guid = mm_metadata_tvshow_guid'
                           ' group by mm_metadata_tvshow_guid')
    sql_data = self.db_cursor.fetchall()
    if sql_data is None:
        return 0
    return len(sql_data)
