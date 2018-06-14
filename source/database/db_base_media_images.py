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


def db_media_images_list_count(self, search_value=None):
    """
    Images list count
    """
    self.db_cursor.execute('select count(*) from mm_media,mm_media_class'
                           ' where mm_media.mm_media_class_guid'
                           ' = mm_media_class.mm_media_class_guid'
                           ' and mm_media_class_type = \'Picture\'')


def db_media_images_list(self, offset=None, records=None, search_value=None):
    """
    Images list
    """
    if offset is None:
        self.db_cursor.execute('select mm_media_path from mm_media,mm_media_class'
                               ' where mm_media.mm_media_class_guid'
                               ' = mm_media_class.mm_media_class_guid'
                               ' and mm_media_class_type = \'Picture\'')
    else:
        self.db_cursor.execute('select mm_media_path from mm_media,mm_media_class'
                               ' where mm_media.mm_media_class_guid'
                               ' = mm_media_class.mm_media_class_guid'
                               ' and mm_media_class_type = \'Picture\' offset %s limit %s',
                               (offset, records))
    return self.db_cursor.fetchall()
