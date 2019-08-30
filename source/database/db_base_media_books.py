"""
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
"""


def db_media_book_list_count(self, search_value=None):
    """
    book list count
    """
    if search_value is not None:
        self.db_cursor.execute('select count(*) from mm_metadata_book, mm_media'
                               ' where mm_media_metadata_guid = mm_metadata_book_guid '
                               'and mm_metadata_book_name %% %s', (search_value,))
    else:
        self.db_cursor.execute('select count(*) from mm_metadata_book, mm_media'
                               ' where mm_media_metadata_guid = mm_metadata_book_guid')
    return self.db_cursor.fetchone()[0]


def db_media_book_list(self, offset=0, records=None, search_value=None):
    """
    book list
    """
    if search_value is not None:
        self.db_cursor.execute('select mm_metadata_book_guid,mm_metadata_book_name '
                               'from mm_metadata_book, mm_media'
                               ' where mm_media_metadata_guid = mm_metadata_book_guid '
                               ' and mm_metadata_book_name %% %s'
                               ' order by LOWER(mm_metadata_book_name)'
                               ' offset %s limit %s', (search_value, offset, records))
    else:
        self.db_cursor.execute('select mm_metadata_book_guid,mm_metadata_book_name '
                               'from mm_metadata_book, mm_media'
                               ' where mm_media_metadata_guid = mm_metadata_book_guid'
                               ' order by LOWER(mm_metadata_book_name)'
                               ' offset %s limit %s', (offset, records))
    return self.db_cursor.fetchall()
