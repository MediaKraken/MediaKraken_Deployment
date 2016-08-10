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

import json
import uuid
import logging


# insert iradio channel
def MK_Server_Database_iRadio_Insert(self, radio_channel):
    if self.sql3_cursor.execute(u'select count(*) from mm_radio where mm_radio_adress = %s', (radio_channel,)):
        if self.sql3_cursor.fetchall()[0][0] == 0:
            self.sql3_cursor.execute(u'insert into mm_radio (mm_radio_guid,mm_radio_adress,mm_radio_active) values (%s,%s,true)', (str(uuid.uuid4()), radio_channel))


# iradio count
def MK_Server_Database_iRadio_List_Count(self, active_station=True):
    self.sql3_cursor.execute(u'select count(*) from mm_radio where mm_radio_active = %s', (active_station,))
    return self.sql3_cursor.fetchone()[0]


# iradio list
def MK_Server_Database_iRadio_List(self, active_station=True, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute(u'select mm_radio_guid, mm_radio_name, mm_radio_adress from mm_radio where mm_radio_active = %s order by LOWER(mm_radio_name)', (active_station,))
    else:
        self.sql3_cursor.execute(u'select mm_radio_guid, mm_radio_name, mm_radio_adress from mm_radio where mm_radio_guid in (select mm_radio_guid from mm_radio where mm_radio_active = %s order by LOWER(mm_radio_name) offset %s limit %s) order by LOWER(mm_radio_name)', (active_station, offset, records))
    return self.sql3_cursor.fetchall()
