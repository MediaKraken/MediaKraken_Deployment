'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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


# query to see if song is in local DB
def MK_Server_Database_Metadata_Music_Video_Lookup(self, artist_name, song_title):
    self.sql3_cursor.execute(u'select mm_metadata_music_video_guid from mm_metadata_music_video where lower(mm_media_music_video_band) = %s and lower(mm_media_music_video_song) = %s', (artist_name.lower(), song_title.lower()))
    return self.sql3_cursor.fetchall()


def MK_Server_Database_Metadata_Music_Video_Add(self, artist_name, artist_song, id_json, data_json, image_json):
    self.sql3_cursor.execute(u'insert into mm_metadata_music_video (mm_metadata_music_video_guid, mm_metadata_music_video_media_id, mm_media_music_video_band, mm_media_music_video_song, mm_metadata_music_video_json, mm_metadata_music_video_localimage_json) values (%s,%s,%s,%s,%s,%s)', (str(uuid.uuid4()), id_json, artist_name, artist_song, data_json, image_json))


def MK_Server_Database_Metadata_Music_Video_Detail_By_UUID(self, item_guid):
    self.sql3_cursor.execute(u'select mm_media_music_video_band, mm_media_music_video_song, mm_metadata_music_video_json, mm_metadata_music_video_localimage_json from mm_metadata_music_video where mm_metadata_music_video_guid = %s', (item_guid,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


def MK_Server_Database_Metadata_Music_Video_Count(self, IMVDb_ID=None):
    if IMVDb_ID is None:
        self.sql3_cursor.execute(u'select count(*) from mm_metadata_music_video')
    else:
        self.sql3_cursor.execute(u'select count(*) from mm_metadata_music_video where mm_metadata_music_video_media_id->\'IMVDb\' ? %s', (IMVDb_ID,))
    return self.sql3_cursor.fetchone()[0]


def MK_Server_Database_Metadata_Music_Video_List(self, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute(u'select mm_metadata_music_video_guid, mm_media_music_video_band, mm_media_music_video_song, mm_metadata_music_video_localimage_json from mm_metadata_music_video order by mm_media_music_video_band, mm_media_music_video_song')
    else:
        self.sql3_cursor.execute(u'select mm_metadata_music_video_guid, mm_media_music_video_band, mm_media_music_video_song, mm_metadata_music_video_localimage_json from mm_metadata_music_video order by mm_media_music_video_band, mm_media_music_video_song offset %s limit %s ', (offset, records))
    return self.sql3_cursor.fetchall()
