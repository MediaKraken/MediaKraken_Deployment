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


# import uuid


def db_meta_sports_guid_by_thesportsdb(self, thesports_uuid):
    """
    # metadata guid by imdb id
    """
    self.db_cursor.execute('select mm_metadata_sports_guid from mm_metadata_sports'
                           ' where mm_metadata_media_sports_id->\'thesportsdb\' ? %s',
                           (thesports_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_sports_guid']
    except:
        return None


def db_meta_sports_list_count(self, search_value=None):
    """
    Count sport events
    """
    if search_value is not None:
        self.db_cursor.execute('select count(*) from mm_metadata_sports'
                               ' where mm_metadata_sports_name %% %s', (search_value,))
    else:
        self.db_cursor.execute('select count(*) from mm_metadata_sports')
    return self.db_cursor.fetchone()[0]


def db_meta_sports_list(self, offset=None, records=None, search_value=None):
    """
    # return list of game systems
    """
    if offset is None:
        if search_value is not None:
            self.db_cursor.execute('select mm_metadata_sports_guid,mm_metadata_sports_name'
                                   ' from mm_metadata_sports where mm_metadata_sports_name %% %s '
                                   'order by mm_metadata_sports_name', (search_value,))
        else:
            self.db_cursor.execute('select mm_metadata_sports_guid,mm_metadata_sports_name'
                                   ' from mm_metadata_sports order by mm_metadata_sports_name')
    else:
        if search_value is not None:
            self.db_cursor.execute('select mm_metadata_sports_guid,mm_metadata_sports_name'
                                   ' from mm_metadata_sports where mm_metadata_sports_guid'
                                   ' in (select mm_metadata_sports_guid from mm_metadata_sports'
                                   ' where mm_metadata_sports_name %% %s'
                                   ' order by mm_metadata_sports_name offset %s limit %s)'
                                   ' order by mm_metadata_sports_name',
                                   (search_value, offset, records))
        else:
            self.db_cursor.execute('select mm_metadata_sports_guid,mm_metadata_sports_name'
                                   ' from mm_metadata_sports where mm_metadata_sports_guid'
                                   ' in (select mm_metadata_sports_guid from mm_metadata_sports'
                                   ' order by mm_metadata_sports_name offset %s limit %s)'
                                   ' order by mm_metadata_sports_name', (offset, records))
    return self.db_cursor.fetchall()


def db_meta_sports_guid_by_event_name(self, event_name):
    """
    # fetch guid by event name
    """
    self.db_cursor.execute('select mm_metadata_sports_guid from mm_metadata_sports'
                           ' where mm_metadata_sports_name = %s', (event_name,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_sports_guid']
    except:
        return None
