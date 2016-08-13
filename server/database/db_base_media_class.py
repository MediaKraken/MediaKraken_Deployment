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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging


def srv_db_media_class_list_count(self):
    """
    Count media class
    """
    self.sql3_cursor.execute('select count(*) from mm_media_class')
    return self.sql3_cursor.fetchone()[0]


def srv_db_media_class_list(self, offset=None, records=None):
    """
    List media class
    """
    if offset is None:
        self.sql3_cursor.execute('select mm_media_class_type,mm_media_class_guid,mm_media_class_display from mm_media_class order by LOWER(mm_media_class_type)')
    else:
        self.sql3_cursor.execute('select mm_media_class_type,mm_media_class_guid,mm_media_class_display from mm_media_class where mm_media_class_guid in (select mm_media_class_guid from mm_media_class order by LOWER(mm_media_class_type) offset %s limit %s) order by LOWER(mm_media_class_type)', (offset, records))
    return self.sql3_cursor.fetchall()


def srv_db_media_class_by_uuid(self, class_uuid):
    """
    Find the class text by uuid
    """
    self.sql3_cursor.execute('select mm_media_class_type from mm_media_class where mm_media_class_guid = %s', (class_uuid,))
    try:
        return self.sql3_cursor.fetchone()['mm_media_class_type']
    except:
        return None


def srv_db_media_uuid_by_class(self, class_text):
    """
    Find the class uuid by class text
    """
    self.sql3_cursor.execute('select mm_media_class_guid from mm_media_class where mm_media_class_type = %s', (class_text,))
    try:
        return self.sql3_cursor.fetchone()['mm_media_class_guid']
    except:
        return None
