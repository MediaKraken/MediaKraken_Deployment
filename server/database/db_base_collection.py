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
import json
import logging


# find all known media
def MK_Server_Database_Collection_List(self, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute(u'select mm_metadata_collection_guid,mm_metadata_collection_name,mm_metadata_collection_imagelocal_json from mm_metadata_collection order by mm_metadata_collection_name')
    else:
        self.sql3_cursor.execute(u'select mm_metadata_collection_guid,mm_metadata_collection_name,mm_metadata_collection_imagelocal_json from mm_metadata_collection where mm_metadata_collection_guid in (select mm_metadata_collection_guid from mm_metadata_collection order by mm_metadata_collection_name offset %s limit %s) order by mm_metadata_collection_name', (offset, records))
    return self.sql3_cursor.fetchall()


# read collection data from json metadata
def MK_Server_Database_Media_Collection_Scan(self):
    self.sql3_cursor.execute(u'select mm_metadata_guid, mm_metadata_json from mm_metadata_movie where mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->>\'belongs_to_collection\'::text <> \'{}\'::text order by mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->>\'belongs_to_collection\'')
    return self.sql3_cursor.fetchall()


# find guid of collection name
def MK_Server_Database_Collection_GUID_By_Name(self, collection_name):
    self.sql3_cursor.execute(u'select mm_metadata_collection_guid from mm_metadata_collection where mm_metadata_collection_name->>\'name\' = %s', (collection_name,))
    try:
        return self.sql3_cursor.fetchone()['mm_metadata_collection_guid']
    except:
        return None


# find guid of collection name
def MK_Server_Database_Collection_By_TMDB(self, tmdb_id):
    self.sql3_cursor.execute(u'select mm_metadata_collection_guid from mm_metadata_collection where mm_metadata_collection_json @> \'{"id":%s}\'', (tmdb_id,))
    try:
        return self.sql3_cursor.fetchone()['mm_metadata_collection_guid']
    except:
        return None


# insert collection
def MK_Server_Database_Collection_Insert(self, collection_name, guid_json, metadata_json, localimage_json):
    self.sql3_cursor.execute(u'insert into mm_metadata_collection (mm_metadata_collection_guid, mm_metadata_collection_name, mm_metadata_collection_media_ids, mm_metadata_collection_json, mm_metadata_collection_imagelocal_json) values (%s,%s,%s,%s,%s)', (str(uuid.uuid4()), json.dumps(collection_name), json.dumps(guid_json), json.dumps(metadata_json), json.dumps(localimage_json)))


# update collection ids
def MK_Server_Database_Collection_Update(self, collection_guid, guid_json):
    self.sql3_cursor.execute(u'update mm_metadata_collection set mm_metadata_collection_media_ids = %s, mm_metadata_collection_json = %s where mm_metadata_collection_guid = %s', (json.dumps(guid_json), collection_guid))


# pull in colleciton info
def MK_Server_Database_Collection_Read_By_GUID(self, media_uuid):
    self.sql3_cursor.execute(u'select mm_metadata_collection_json,mm_metadata_collection_imagelocal_json from mm_metadata_collection where mm_metadata_collection_guid = %s', (media_uuid,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None

