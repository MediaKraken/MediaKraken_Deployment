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
import logging # pylint: disable=W0611
import uuid


def db_device_count(self):
    """
    Return the number of devices in database
    """
    self.db_cursor.execute('select count(*) from mm_device')
    return self.db_cursor.fetchone()[0]


def db_device_list(self, device_type=None, offset=None, records=None):
    """
    Return list of devices in database
    """
    if device_type is None:
        if offset is None:
            self.db_cursor.execute('select mm_device_id, mm_device_type, mm_device_json'\
                ' from mm_device')
        else:
            self.db_cursor.execute('select mm_device_id, mm_device_type, mm_device_json'\
                ' from mm_device offset %s limit %s', (offset, records))
    else:
        if offset is None:
            self.db_cursor.execute('select mm_device_id, mm_device_type, mm_device_json'\
                ' from mm_device where mm_device_type = %s', (device_type,))
        else:
            self.db_cursor.execute('select mm_device_id, mm_device_type, mm_device_json'\
                ' from mm_device where mm_device_type = %s offset %s limit %s',\
                (device_type, offset, records))
    return self.db_cursor.fetchall()


def db_device_insert(self, device_type, device_json):
    """
    Insert a device into the database
    """
    self.db_cursor.execute('insert into mm_device (mm_device_id, mm_device_type,'\
        ' mm_device_json) values (%s,%s,%s)', (str(uuid.uuid4()), device_type, device_json))


def db_device_update(self, guid, device_type, device_json):
    """
    Update the device in the database
    """
    self.db_cursor.execute('update mm_device set mm_device_type = %s, mm_device_json = %s'\
        ' where mm_device_id = %s', (device_type, device_json, guid))


def db_device_delete(self, guid):
    """
    Remove a device from the database via uuid
    """
    self.db_cursor.execute('delete from mm_device where mm_device_id = %s', (guid,))


def db_device_read(self, guid):
    """
    Return details from database via uuid
    """
    self.db_cursor.execute('select mm_device_type, mm_device_json from mm_device'\
        ' where mm_device_id = %s', (guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None
