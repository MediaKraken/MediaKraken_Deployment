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

import uuid


def db_media_class_insert(self, class_name, class_type, display_class):
    """
    insert media class
    """
    new_media_class_uuid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_media_class (mm_media_class_guid,'
                           'mm_media_class_type,mm_media_class_parent_type,'
                           'mm_media_class_display) values (%s,%s,%s,%s)',
                           (new_media_class_uuid, class_name, class_type, display_class))
    self.db_commit()
    return new_media_class_uuid


def db_media_class_list_count(self):
    """
    Count media class
    """
    self.db_cursor.execute('select count(*) from mm_media_class')
    return self.db_cursor.fetchone()[0]


def db_media_class_list(self, offset=0, records='ALL'):
    """
    List media class
    """
    self.db_cursor.execute('select mm_media_class_type,mm_media_class_guid,'
                           'mm_media_class_display from mm_media_class'
                           ' where mm_media_class_guid'
                           ' in (select mm_media_class_guid from mm_media_class'
                           ' order by LOWER(mm_media_class_type) offset %s limit %s)'
                           ' order by LOWER(mm_media_class_type)', (offset, records))
    return self.db_cursor.fetchall()


def db_media_class_by_uuid(self, class_uuid):
    """
    Find the class text by uuid
    """
    self.db_cursor.execute('select mm_media_class_type from mm_media_class'
                           ' where mm_media_class_guid = %s', (class_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_media_class_type']
    except:
        return None


def db_media_uuid_by_class(self, class_text):
    """
    Find the class uuid by class text
    """
    self.db_cursor.execute('select mm_media_class_guid from mm_media_class'
                           ' where mm_media_class_type = %s', (class_text,))
    try:
        return self.db_cursor.fetchone()['mm_media_class_guid']
    except:
        return None
