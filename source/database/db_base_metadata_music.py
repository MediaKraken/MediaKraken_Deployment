"""
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
"""

import uuid


def db_meta_song_list(self, offset=0, records=None, search_value=None):
    """
    # return songs metadatalist
    """
    # TODO, only grab the poster locale from json
    return self.db_cursor.fetchall()


def db_music_lookup(self, artist_name, album_name, song_title):
    """
    # query to see if song is in local DB
    """
    # TODO the following fields don't exist on the database (album and musician)
    # TODO order by release year
    self.db_cursor.execute('select mm_metadata_music_guid,'
                           ' mm_metadata_media_music_id->\'Mbrainz\' as mbrainz from '
                           'mm_metadata_music,'
                           ' mm_metadata_album, mm_metadata_musician'
                           ' where lower(mm_metadata_musician_name) = %s'
                           ' and lower(mm_metadata_album_name) = %s'
                           ' and lower(mm_metadata_music_name) = %s',
                           (artist_name.lower(), album_name.lower(), song_title.lower()))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_meta_musician_by_guid(self, guid):
    """
    # return musician data by guid
    """
    self.db_cursor.execute('select * from mm_metadata_musician'
                           ' where mm_metadata_musician_guid = %s', (guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_meta_musician_add(self, data_name, data_id, data_json):
    """
    # insert musician
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_metadata_musician (mm_metadata_musician_guid,'
                           ' mm_metadata_musician_name, mm_metadata_musician_id,'
                           ' mm_metadata_musician_json) values (%s,%s,%s,%s)',
                           (new_guid, data_name, data_id, data_json))
    self.db_commit()
    return new_guid


def db_meta_album_by_guid(self, guid):
    """
    # return album data by guid
    """
    self.db_cursor.execute('select * from mm_metadata_album where mm_metadata_album_guid = %s',
                           (guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_meta_album_add(self, data_name, data_id, data_json):
    """
    # insert album
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_metadata_album (mm_metadata_album_guid,'
                           ' mm_metadata_album_name, mm_metadata_album_id,'
                           ' mm_metadata_album_json) values (%s,%s,%s,%s)',
                           (new_guid, data_name, data_id, data_json))
    self.db_commit()
    return new_guid


def db_meta_song_by_guid(self, guid):
    """
    # return song data by guid
    """
    self.db_cursor.execute('select * from mm_metadata_music where mm_metadata_music_guid = %s',
                           (guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_meta_song_add(self, data_name, data_id, data_json):
    """
    # insert song
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_metadata_music (mm_metadata_music_guid,'
                           ' mm_metadata_music_name, mm_metadata_media_music_id,'
                           ' mm_metadata_music_json) values (%s,%s,%s,%s)',
                           (new_guid, data_name, data_id, data_json))
    self.db_commit()
    return new_guid


def db_meta_songs_by_album_guid(self, guid):
    """
    # return song list from ablum guid
    """
    self.db_cursor.execute('select * from mm_metadata_music where blah = %s'
                           ' order by lower(mm_metadata_music_name)', (guid,))
    return self.db_cursor.fetchall()


def db_meta_album_list(self, offset=0, records=None, search_value=None):
    """
    # return albums metadatalist
    """
    # TODO, only grab the poster locale from json
    # TODO order by release year
    if search_value is not None:
        self.db_cursor.execute('select mm_metadata_album_guid, mm_metadata_album_name,'
                               ' mm_metadata_album_json, mm_metadata_album_image'
                               ' from mm_metadata_album'
                               ' where mm_metadata_album_name %% %s'
                               ' order by LOWER(mm_metadata_album_name)'
                               ' offset %s limit %s', (search_value, offset, records))
    else:
        self.db_cursor.execute('select mm_metadata_album_guid, mm_metadata_album_name,'
                               ' mm_metadata_album_json, mm_metadata_album_image'
                               ' from mm_metadata_album'
                               ' order by LOWER(mm_metadata_album_name)'
                               ' offset %s limit %s', (offset, records))
    return self.db_cursor.fetchall()


def db_meta_muscian_list(self, offset=0, records=None, search_value=None):
    """
    # return muscian metadatalist
    """
    # TODO, only grab the poster locale from json
    if search_value is not None:
        self.db_cursor.execute('select mm_metadata_musician_guid, mm_metadata_musician_name,'
                               ' mm_metadata_musician_json from mm_metadata_musician'
                               ' where mm_metadata_musician_name %% %s'
                               ' order by LOWER(mm_metadata_musician_name) offset %s limit %s',
                               (search_value, offset, records))
    else:
        self.db_cursor.execute('select mm_metadata_musician_guid, mm_metadata_musician_name,'
                               ' mm_metadata_musician_json from mm_metadata_musician'
                               ' order by LOWER(mm_metadata_musician_name) offset %s limit %s',
                               (offset, records))
    return self.db_cursor.fetchall()


def db_meta_album_image_random(self):
    """
    Find random album cover image
    """
    # self.db_cursor.execute('select mm_metadata_localimage_json->\'Images\'->\'themoviedb\'->>\''
    #     + return_image_type + '\' as image_json,mm_metadata_guid from mm_media,mm_metadata_movie'\
    #     ' where mm_media_metadata_guid = mm_metadata_guid'\
    #     ' and (mm_metadata_localimage_json->\'Images\'->\'themoviedb\'->>\''
    #     + return_image_type + '\'' + ')::text != \'null\' order by random() limit 1')
    try:
        # then if no results.....a None will except which will then pass None, None
        image_json, metadata_id = self.db_cursor.fetchone()
        return image_json, metadata_id
    except:
        return None, None


def db_meta_music_by_provider_uuid(self, provider, uuid_id):
    try:
        self.db_cursor.execute('select mm_metadata_music_guid from mm_metadata_music'
                               ' where mm_metadata_media_music_id->\'' + provider
                               + '\' ? %s', (uuid_id,))
        return self.db_cursor.fetchone()['mm_metadata_music_guid']
    except:
        return None
