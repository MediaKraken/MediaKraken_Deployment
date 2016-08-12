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
import json
import uuid


def srv_db_iradio_insert(self, radio_channel):
    """
    Insert iradio channel
    """
    if self.sql3_cursor.execute('select count(*) from mm_radio where mm_radio_adress = %s',\
        (radio_channel,)):
        if self.sql3_cursor.fetchall()[0][0] == 0:
            self.sql3_cursor.execute('insert into mm_radio (mm_radio_guid,mm_radio_adress,'\
                'mm_radio_active) values (%s,%s,true)', (str(uuid.uuid4()), radio_channel))


def srv_db_iradio_list_count(self, active_station=True):
    """
    Iradio count
    """
    self.sql3_cursor.execute('select count(*) from mm_radio where mm_radio_active = %s',\
        (active_station,))
    return self.sql3_cursor.fetchone()[0]


def srv_db_iradio_list(self, active_station=True, offset=None, records=None):
    """
    Iradio list
    """
    if offset is None:
        self.sql3_cursor.execute('select mm_radio_guid, mm_radio_name, mm_radio_adress'\
            ' from mm_radio where mm_radio_active = %s order by LOWER(mm_radio_name)',\
            (active_station,))
    else:
        self.sql3_cursor.execute('select mm_radio_guid, mm_radio_name, mm_radio_adress'\
            ' from mm_radio where mm_radio_guid in (select mm_radio_guid from mm_radio'\
            ' where mm_radio_active = %s order by LOWER(mm_radio_name) offset %s limit %s)'\
            ' order by LOWER(mm_radio_name)',\
        (active_station, offset, records))
    return self.sql3_cursor.fetchall()
