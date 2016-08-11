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


# count tuners
def MK_Server_Database_Tuner_Count(self):
    self.sql3_cursor.execute('select count(*) from mm_tuner')
    return self.sql3_cursor.fetchone()[0]


# read tuners
def MK_Server_Database_Tuner_List(self, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute('select mm_tuner_id, mm_tuner_json from mm_tuner')
    else:
        self.sql3_cursor.execute('select mm_tuner_id, mm_tuner_json from mm_tuner offset %s limit %s', (offset, records))
    return self.sql3_cursor.fetchall()


# insert record
def MK_Server_Database_Tuner_Insert(self, tuner_json):
    self.sql3_cursor.execute('insert into mm_tuner (mm_tuner_id, mm_tuner_json) values (%s,%s)', (str(uuid.uuid4()), tuner_json))


# update record
def MK_Server_Database_Tuner_Update(self, guid, tuner_json):
    self.sql3_cursor.execute('update mm_tuner set mm_tuner_json = %s where mm_tuner_id = %s', (tuner_json, guid))


# delete record
def MK_Server_Database_Tuner_Delete(self, guid):
    self.sql3_cursor.execute('delete from mm_tuner where mm_tuner_id = %s', (guid,))


# find detials by hardware id (serial)
def MK_Server_Database_Tuner_By_Serial(self, serial_no):
    self.sql3_cursor.execute('select mm_tuner_id, mm_tuner_json from mm_tuner where mm_tuner_json->\'ID\' ? %s', (serial_no,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None

