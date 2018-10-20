'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

# this is to hold the ir/network codes for specific hardware devices!d

def db_hardware_json_read(self, manufacturer, model_name):
    """
    Return json for machine/model
    """
    self.db_cursor.execute('select mm_hardware_json from mm_hardware_json'
                           ' where mm_hardware_manufacturer %% %s'
                           ' and mm_hardware_model %% %s',
                           (manufacturer, model_name))
    return self.db_cursor.fetchone()[0]


def db_hardware_insert(self, manufacturer, model_name, json_data):
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_hardware_json (mm_hardware_id,'
                           ' mm_hardware_manufacturer, mm_hardware_model,'
                           ' mm_hardware_json) values (%s, %s, %s, %s)',
                           (new_guid, manufacturer, model_name, json_data))
    self.db_commit()
    return new_guid


def db_hardware_delete(self, guid):
    self.db_cursor.execute('delete from mm_hardware_json where mm_hardware_id = %s', (guid,))
    self.db_commit()
