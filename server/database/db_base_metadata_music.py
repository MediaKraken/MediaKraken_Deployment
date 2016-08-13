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
#import logging
import uuid


def srv_db_music_lookup(self, artist_name, album_name, song_title):
    """
    # query to see if song is in local DB
    """
    self.sql3_cursor.execute('select mm_metadata_music_guid,'\
        ' mm_metadata_media_music_id->\'Mbrainz\' from mm_metadata_music, mm_metadata_album,'\
        ' mm_metadata_musician where blah and lower(mm_metadata_musician_name) = %s'\
        ' and lower(mm_metadata_album_name) = %s and lower(mm_metadata_music_name) = %s',\
        (artist_name.lower(), album_name.lower(), song_title.lower()))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


def srv_db_meta_musician_by_guid(self, guid):
    """
    # return musician data by guid
    """
    self.sql3_cursor.execute('select * from mm_metadata_musician'\
        ' where mm_metadata_musician_guid = %s', (guid,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


def srv_db_meta_musician_add(self, data_name, data_id, data_json):
    """
    # insert musician
    """
    self.sql3_cursor.execute('insert into mm_metadata_musician (mm_metadata_musician_guid,'\
        ' mm_metadata_musician_name, mm_metadata_musician_id, mm_metadata_musician_json)'\
        ' values (%s,%s,%s,%s)', (str(uuid.uuid4()), data_name, data_id, data_json))


def srv_db_meta_album_by_guid(self, guid):
    """
    # return album data by guid
    """
    self.sql3_cursor.execute('select * from mm_metadata_album where mm_metadata_album_guid = %s',\
        (guid,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


def srv_db_meta_album_add(self, data_name, data_id, data_json):
    """
    # insert album
    """
    self.sql3_cursor.execute('insert into mm_metadata_album (mm_metadata_album_guid,'\
        ' mm_metadata_album_name, mm_metadata_album_id, mm_metadata_album_json)'\
        ' values (%s,%s,%s,%s)', (str(uuid.uuid4()), data_name, data_id, data_json))


def srv_db_meta_song_by_guid(self, guid):
    """
    # return song data by guid
    """
    self.sql3_cursor.execute('select * from mm_metadata_music where mm_metadata_music_guid = %s',\
        (guid,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


def srv_db_meta_song_add(self, data_name, data_id, data_json):
    """
    # insert song
    """
    self.sql3_cursor.execute('insert into mm_metadata_music (mm_metadata_music_guid,'\
        ' mm_metadata_music_name, mm_metadata_media_music_id, mm_metadata_music_json)'\
        ' values (%s,%s,%s,%s)', (str(uuid.uuid4()), data_name, data_id, data_json))


def srv_db_meta_songs_by_album_guid(self, guid):
    """
    # return song list from ablum guid
    """
    self.sql3_cursor.execute('select * from mm_metadata_music where blah = %s'\
        ' order by lower(mm_metadata_music_name)', (guid,))
    return self.sql3_cursor.fetchall()


def srv_db_meta_album_list(self, offset=None, records=None):
    """
    # return albums metadatalist
    """
    # TODO, only grab the poster local from json
    if offset is None:
        self.sql3_cursor.execute('select mm_metadata_album_guid, mm_metadata_album_name,'\
            ' mm_metadata_album_json from mm_metadata_album order by mm_metadata_album_name')
    else:
        self.sql3_cursor.execute('select mm_metadata_album_guid, mm_metadata_album_name,'\
            ' mm_metadata_album_json from mm_metadata_album order by mm_metadata_album_name'\
            ' offset %s limit %s', (offset, records))
    return self.sql3_cursor.fetchall()
        

def srv_db_meta_muscian_list(self, offset=None, records=None):
    """
    # return muscian metadatalist
    """
    # TODO, only grab the poster local from json
    if offset is None:
        self.sql3_cursor.execute('select mm_metadata_musician_guid, mm_metadata_musician_name,'\
            ' mm_metadata_musician_json from mm_metadata_musician'\
            ' order by mm_metadata_musician_name')
    else:
        self.sql3_cursor.execute('select mm_metadata_musician_guid, mm_metadata_musician_name,'\
            ' mm_metadata_musician_json from mm_metadata_musician'\
            ' order by mm_metadata_musician_name offset %s limit %s', (offset, records))
    return self.sql3_cursor.fetchall()
