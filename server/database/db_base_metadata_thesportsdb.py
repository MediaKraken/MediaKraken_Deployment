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
import logging


# select
def MK_Server_Database_MetadataTheSportsDB_Select_By_Guid(self, guid):
    self.sql3_cursor.execute(u'select mm_metadata_sports_json from mm_metadata_sports where mm_metadata_sports_guid = %s', (guid,))
    try:
        return self.sql3_cursor.fetchone()['mm_metadata_sports_json']
    except:
        return None


# insert
def MK_Server_Database_MetadataTheSportsDB_Insert(self, series_id_json, event_name, show_detail, image_json):
    self.sql3_cursor.execute(u'insert into mm_metadata_sports (mm_metadata_sports_guid, mm_metadata_media_sports_id, mm_metadata_sports_name, mm_metadata_sports_json, mm_metadata_sports_image_json) values (%s,%s,%s,%s,%s)', (str(uuid.uuid4()), series_id_json, event_name, show_detail, image_json))


# updated
def MK_Server_Database_MetadataTheSports_Update(self, series_id_json, event_name, show_detail, sportsdb_id):
    self.sql3_cursor.execute(u'update mm_metadata_sports set mm_metadata_media_sports_id = %s, mm_metadata_sports_name = %s, mm_metadata_sports_json = %s where mm_metadata_media_sports_id->\'TheSportsDB\' ? %s', (series_id_json, event_name, show_detail, sportsdb_id))
