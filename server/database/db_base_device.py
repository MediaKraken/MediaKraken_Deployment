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
import logging
import uuid


def MK_Server_Database_Device_Count(self):
    """
    Return the number of devices in database
    """
    self.sql3_cursor.execute('select count(*) from mm_device')
    return self.sql3_cursor.fetchone()[0]


def MK_Server_Database_Device_List(self, device_type=None, offset=None, records=None):
    """
    Return list of devices in database
    """
    if device_type is None:
        if offset is None:
            self.sql3_cursor.execute('select mm_device_id, mm_device_type, mm_device_json from mm_device')
        else:
            self.sql3_cursor.execute('select mm_device_id, mm_device_type, mm_device_json from mm_device offset %s limit %s', (offset, records))
    else:
        if offset is None:
            self.sql3_cursor.execute('select mm_device_id, mm_device_type, mm_device_json from mm_device where mm_device_type = %s', (device_type,))
        else:
            self.sql3_cursor.execute('select mm_device_id, mm_device_type, mm_device_json from mm_device where mm_device_type = %s offset %s limit %s', (device_type, offset, records))
    return self.sql3_cursor.fetchall()


def MK_Server_Database_Device_Insert(self, device_type, device_json):
    """
    Insert a device into the database
    """
    self.sql3_cursor.execute('insert into mm_device (mm_device_id, mm_device_type, mm_device_json) values (%s,%s,%s)', (str(uuid.uuid4()), device_type, device_json))


def MK_Server_Database_Device_Update(self, guid, device_type, device_json):
    """
    Update the device in the database
    """
    self.sql3_cursor.execute('update mm_device set mm_device_type = %s, mm_device_json = %s where mm_device_id = %s', (device_type, device_json, guid))


def MK_Server_Database_Device_Delete(self, guid):
    """
    Remove a device from the database via uuid
    """
    self.sql3_cursor.execute('delete from mm_device where mm_device_id = %s', (guid,))


def MK_Server_Database_Device_Read(self, guid):
    """
    Return details from database via uuid
    """
    self.sql3_cursor.execute('select mm_device_type, mm_device_json from mm_device where mm_device_id = %s', (guid,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None

