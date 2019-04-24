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


def db_iradio_insert(self, radio_channel):
    """
    Insert iradio channel
    """
    if self.db_cursor.execute('select count(*) from mm_radio where mm_radio_adress = %s',
                              (radio_channel,)):
        if self.db_cursor.fetchall()[0][0] == 0:
            new_guid = str(uuid.uuid4())
            self.db_cursor.execute('insert into mm_radio (mm_radio_guid,mm_radio_adress,'
                                   'mm_radio_active) values (%s,%s,true)',
                                   (new_guid, radio_channel))
            self.db_commit()
            return new_guid


def db_iradio_list_count(self, active_station=True, search_value=None):
    """
    Iradio count
    """
    if search_value is not None:
        self.db_cursor.execute('select count(*) from mm_radio '
                               'where mm_radio_active = %s and mm_radio_name %% %s',
                               (active_station,))
    else:
        self.db_cursor.execute('select count(*) from mm_radio where mm_radio_active = %s',
                               (active_station,))
    return self.db_cursor.fetchone()[0]


def db_iradio_list(self, offset=0, records='ALL', active_station=True, search_value=None):
    """
    Iradio list
    """
    if search_value is not None:
        self.db_cursor.execute('select mm_radio_guid, mm_radio_name, mm_radio_adress'
                               ' from mm_radio where mm_radio_guid '
                               'in (select mm_radio_guid from mm_radio'
                               ' where mm_radio_active = %s and mm_radio_name %% %s'
                               ' order by LOWER(mm_radio_name) offset %s limit %s)'
                               ' order by LOWER(mm_radio_name)',
                               (active_station, search_value, offset, records))
    else:
        self.db_cursor.execute('select mm_radio_guid, mm_radio_name, mm_radio_adress'
                               ' from mm_radio where mm_radio_guid'
                               ' in (select mm_radio_guid from mm_radio'
                               ' where mm_radio_active = %s order by LOWER(mm_radio_name)'
                               ' offset %s limit %s) order by LOWER(mm_radio_name)',
                               (active_station, offset, records))
    return self.db_cursor.fetchall()
