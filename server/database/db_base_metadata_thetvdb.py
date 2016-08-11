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
import json


# insert
def MK_Server_Database_MetadataTVDB_Insert(self, series_id_json, tv_name, show_detail, image_json):
    media_uuid = str(uuid.uuid4())
    self.sql3_cursor.execute(u'insert into mm_metadata_tvshow (mm_metadata_tvshow_guid, mm_metadata_media_tvshow_id, mm_metadata_tvshow_name, mm_metadata_tvshow_json, mm_metadata_tvshow_localimage_json) values (%s,%s,%s,%s,%s)', (media_uuid, series_id_json, tv_name, show_detail, image_json))
    return media_uuid


# updated
def MK_Server_Database_MetadataTVDB_Update(self, series_id_json, tv_name, show_detail, tvdb_id):
    self.sql3_cursor.execute(u'update mm_metadata_tvshow set mm_metadata_media_tvshow_id = %s, mm_metadata_tvshow_name = %s, mm_metadata_tvshow_json = %s where mm_metadata_media_tvshow_id->\'theTVDB\' ? %s', (series_id_json, tv_name, show_detail, tvdb_id))
