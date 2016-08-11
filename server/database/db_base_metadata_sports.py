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
import uuid


# metadata guid by imdb id
def MK_Server_Database_Metadata_Sports_GUID_By_TheSportsDB(self, thesports_uuid):
    self.sql3_cursor.execute('select mm_metadata_sports_guid from mm_metadata_sports where mm_metadata_media_sports_id->\'TheSportsDB\' ? %s', (thesports_uuid,))
    try:
        return self.sql3_cursor.fetchone()['mm_metadata_sports_guid']
    except:
        return None


def MK_Server_Database_Metadata_Sports_List_Count(self):
    self.sql3_cursor.execute('select count(*) from mm_metadata_sports')
    return self.sql3_cursor.fetchone()[0]


# return list of game systems
def MK_Server_Database_Metadata_Sports_List(self, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute('select mm_metadata_sports_guid,mm_metadata_sports_name from mm_metadata_sports order by mm_metadata_sports_name')
    else:
        self.sql3_cursor.execute('select mm_metadata_sports_guid,mm_metadata_sports_name from mm_metadata_sports where mm_metadata_sports_guid in (select mm_metadata_sports_guid from mm_metadata_sports order by mm_metadata_sports_name offset %s limit %s) order by mm_metadata_sports_name', (offset, records))
    return self.sql3_cursor.fetchall()


# fetch guid by event name
def MK_Server_Database_Metadata_Sports_GUID_By_Event_Name(self, event_name):
    self.sql3_cursor.execute('select mm_metadata_sports_guid from mm_metadata_sports where mm_metadata_sports_name = %s', (event_name,))
    try:
        return self.sql3_cursor.fetchone()['mm_metadata_sports_guid']
    except:
        return None
