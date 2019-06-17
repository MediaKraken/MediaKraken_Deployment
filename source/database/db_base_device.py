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

import uuid


def db_device_count(self, device_type=None, search_value=None):
    """
    Return the number of devices in database
    """
    if device_type is None:
        self.db_cursor.execute('select count(*) from mm_device')
    else:
        self.db_cursor.execute('select count(*) from mm_device where mm_device_type = %s',
                               (device_type,))
    return self.db_cursor.fetchone()[0]


def db_device_list(self, device_type=None, offset=0, records=None, search_value=None):
    """
    Return list of devices in database
    """
    if device_type is None:
        self.db_cursor.execute('select mm_device_id, mm_device_type, mm_device_json'
                               ' from mm_device order by mm_device_type'
                               ' offset %s limit %s', (offset, records))
    else:
        self.db_cursor.execute('select mm_device_id, mm_device_type, mm_device_json'
                               ' from mm_device where mm_device_type = %s offset %s limit %s',
                               (device_type, offset, records))
    return self.db_cursor.fetchall()


def db_device_insert(self, device_type, device_json):
    """
    Insert a device into the database
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_device (mm_device_id, mm_device_type,'
                           ' mm_device_json) values (%s,%s,%s)',
                           (new_guid, device_type, device_json))
    return new_guid


def db_device_update(self, guid, device_type, device_json):
    """
    Update the device in the database
    """
    self.db_cursor.execute('update mm_device set mm_device_type = %s, mm_device_json = %s'
                           ' where mm_device_id = %s', (device_type, device_json, guid))


def db_device_delete(self, guid):
    """
    Remove a device from the database via uuid
    """
    self.db_cursor.execute(
        'delete from mm_device where mm_device_id = %s', (guid,))
    self.db_commit()


def db_device_read(self, guid):
    """
    Return details from database via uuid
    """
    self.db_cursor.execute('select mm_device_type, mm_device_json from mm_device'
                           ' where mm_device_id = %s', (guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_device_check(self, device_type, device_name, device_ip):
    """
    Check to see if device exists already on db
    """
    self.db_cursor.execute(
        'select count(*) from mm_device where mm_device_type = %s mm_device_json->\'Name\' ? %s'
        ' and mm_device_json->\'IP\' ? %s', (device_type, device_name, device_ip))
    return self.db_cursor.fetchone()[0]


def db_device_upsert(self, device_type, device_json):
    """
    Upsert a device into the database
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('INSERT INTO mm_device (mm_device_id, mm_device_type,'
                           ' mm_device_json) VALUES (%s, %s, %s)'
                           ' ON CONFLICT ((mm_device_json->>"IP"))'
                           ' DO UPDATE SET mm_device_type = %s, mm_device_json = %s',
                           (new_guid, device_type, device_json, device_type, device_json))
    return new_guid
