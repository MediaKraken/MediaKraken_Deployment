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
import logging  # pylint: disable=W0611
import uuid


def db_tuner_count(self):
    """
    Return count of tuners in database
    """
    self.db_cursor.execute('select count(*) from mm_tuner')
    return self.db_cursor.fetchone()[0]


def db_tuner_list(self, offset=None, records=None):
    """
    Return list of tuners in the database
    """
    if offset is None:
        self.db_cursor.execute('select mm_tuner_id, mm_tuner_json from mm_tuner')
    else:
        self.db_cursor.execute('select mm_tuner_id, mm_tuner_json from mm_tuner'
                               ' offset %s limit %s', (offset, records))
    return self.db_cursor.fetchall()


def db_tuner_insert(self, tuner_json):
    """
    Insert tuner into the database
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_tuner (mm_tuner_id, mm_tuner_json) values (%s,%s)',
                           (new_guid, tuner_json))
    self.db_commit()
    return new_guid


def db_tuner_update(self, guid, tuner_json):
    """
    Update tuner record in the database
    """
    self.db_cursor.execute('update mm_tuner set mm_tuner_json = %s where mm_tuner_id = %s',
                           (tuner_json, guid))
    self.db_commit()


def db_tuner_delete(self, guid):
    """
    Remove tuner from the database
    """
    self.db_cursor.execute('delete from mm_tuner where mm_tuner_id = %s', (guid,))
    self.db_commit()


def db_tuner_by_serial(self, serial_no):
    """
    Find detials by hardware id (serial)
    """
    self.db_cursor.execute('select mm_tuner_id, mm_tuner_json from mm_tuner'
                           ' where mm_tuner_json->\'ID\' ? %s', (serial_no,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None
