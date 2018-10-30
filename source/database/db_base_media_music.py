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


def db_media_album_count(self, search_value=None):
    """
    Album count
    """
    if search_value is not None:
        self.db_cursor.execute('select count(*) from mm_metadata_album, mm_media'
                               ' where mm_media_metadata_guid = mm_metadata_album_guid '
                               ' and mm_metadata_album_name %% %s group by mm_metadata_album_guid',
                               (search_value,))
    else:
        self.db_cursor.execute('select count(*) from mm_metadata_album, mm_media'
                               ' where mm_media_metadata_guid = mm_metadata_album_guid'
                               ' group by mm_metadata_album_guid')
    return self.db_cursor.fetchone()[0]


def db_media_album_list(self, offset=None, per_page=None, search_value=None):
    """
    Album list
    """
    # TODO only grab the image part of the json for list
    if offset is None:
        if search_value is not None:
            self.db_cursor.execute('select mm_metadata_album_guid,mm_metadata_album_name,'
                                   'mm_metadata_album_json from mm_metadata_album, mm_media'
                                   ' where mm_media_metadata_guid = mm_metadata_album_guid '
                                   'and mm_metadata_album_name %% %s'
                                   ' group by mm_metadata_album_guid'
                                   ' order by mm_metadata_album_name',
                                   (search_value,))
        else:
            self.db_cursor.execute('select mm_metadata_album_guid,mm_metadata_album_name,'
                                   'mm_metadata_album_json from mm_metadata_album, mm_media'
                                   ' where mm_media_metadata_guid = mm_metadata_album_guid'
                                   ' group by mm_metadata_album_guid'
                                   ' order by mm_metadata_album_name')
    else:
        if search_value is not None:
            self.db_cursor.execute('select mm_metadata_album_guid,mm_metadata_album_name,'
                                   'mm_metadata_album_json from mm_metadata_album, mm_media'
                                   ' where mm_media_metadata_guid = mm_metadata_album_guid'
                                   ' and mm_metadata_album_name %% %s'
                                   ' group by mm_metadata_album_guid'
                                   ' order by mm_metadata_album_name'
                                   ' offset %s limit %s', (search_value, offset, per_page))
        else:
            self.db_cursor.execute('select mm_metadata_album_guid,mm_metadata_album_name,'
                                   'mm_metadata_album_json from mm_metadata_album, mm_media'
                                   ' where mm_media_metadata_guid = mm_metadata_album_guid'
                                   ' group by mm_metadata_album_guid'
                                   ' order by mm_metadata_album_name'
                                   ' offset %s limit %s', (offset, per_page))
    return self.db_cursor.fetchall()
