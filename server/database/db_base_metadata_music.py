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


# query to see if song is in local DB
def MK_Server_Database_Music_Lookup(self, artist_name, album_name, song_title):
    self.sql3_cursor.execute(u'select mm_metadata_music_guid, mm_metadata_media_music_id->\'Mbrainz\' from mm_metadata_music, mm_metadata_album, mm_metadata_musician where blah and lower(mm_metadata_musician_name) = %s and lower(mm_metadata_album_name) = %s and lower(mm_metadata_music_name) = %s', (artist_name.lower(), album_name.lower(), song_title.lower()))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


# return musician data by guid
def MK_Server_Database_Metadata_Musician_By_GUID(self, guid):
    self.sql3_cursor.execute(u'select * from mm_metadata_musician where mm_metadata_musician_guid = %s', (guid,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


# insert musician
def MK_Server_Database_Metadata_Musician_Add(self, data_name, data_id, data_json):
    self.sql3_cursor.execute(u'insert into mm_metadata_musician (mm_metadata_musician_guid, mm_metadata_musician_name, mm_metadata_musician_id, mm_metadata_musician_json) values (%s,%s,%s,%s)', (str(uuid.uuid4()), data_name, data_id, data_json))


# return album data by guid
def MK_Server_Database_Metadata_Album_By_GUID(self, guid):
    self.sql3_cursor.execute(u'select * from mm_metadata_album where mm_metadata_album_guid = %s', (guid,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


# insert album
def MK_Server_Database_Metadata_Album_Add(self, data_name, data_id, data_json):
    self.sql3_cursor.execute(u'insert into mm_metadata_album (mm_metadata_album_guid, mm_metadata_album_name, mm_metadata_album_id, mm_metadata_album_json) values (%s,%s,%s,%s)', (str(uuid.uuid4()), data_name, data_id, data_json))


# return song data by guid
def MK_Server_Database_Metadata_Song_By_GUID(self, guid):
    self.sql3_cursor.execute(u'select * from mm_metadata_music where mm_metadata_music_guid = %s', (guid,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


# insert song
def MK_Server_Database_Metadata_Song_Add(self, data_name, data_id, data_json):
    self.sql3_cursor.execute(u'insert into mm_metadata_music (mm_metadata_music_guid, mm_metadata_music_name, mm_metadata_media_music_id, mm_metadata_music_json) values (%s,%s,%s,%s)', (str(uuid.uuid4()), data_name, data_id, data_json))


# return song list from ablum guid
def MK_Server_Database_Metadata_Songs_By_Album_GUID(self, guid):
    self.sql3_cursor.execute(u'select * from mm_metadata_music where blah = %s order by lower(mm_metadata_music_name)', (guid,))
    return self.sql3_cursor.fetchall()


# return albums metadatalist
def MK_Server_Database_Metadata_Album_List(self, offset=None, records=None):
    # TODO, only grab the poster local from json
    if offset is None:
        self.sql3_cursor.execute(u'select mm_metadata_album_guid, mm_metadata_album_name, mm_metadata_album_json from mm_metadata_album order by mm_metadata_album_name')
    else:
        self.sql3_cursor.execute(u'select mm_metadata_album_guid, mm_metadata_album_name, mm_metadata_album_json from mm_metadata_album order by mm_metadata_album_name offset %s limit %s', (offset, records))
    return self.sql3_cursor.fetchall()
        

# return muscian metadatalist
def MK_Server_Database_Metadata_Muscian_List(self, offset=None, records=None):
    # TODO, only grab the poster local from json
    if offset is None:
        self.sql3_cursor.execute(u'select mm_metadata_musician_guid, mm_metadata_musician_name, mm_metadata_musician_json from mm_metadata_musician order by mm_metadata_musician_name')
    else:
        self.sql3_cursor.execute(u'select mm_metadata_musician_guid, mm_metadata_musician_name, mm_metadata_musician_json from mm_metadata_musician order by mm_metadata_musician_name offset %s limit %s', (offset, records))
    return self.sql3_cursor.fetchall()
