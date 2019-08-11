"""
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
"""


def db_meta_music_video_lookup(self, artist_name, song_title):
    """
    # query to see if song is in local DB
    """
    self.db_cursor.execute('select mm_metadata_music_video_guid from mm_metadata_music_video'
                           ' where lower(mm_media_music_video_band) = %s'
                           ' and lower(mm_media_music_video_song) = %s',
                           (artist_name.lower(), song_title.lower()))
    return self.db_cursor.fetchall()


def db_meta_music_video_add(self, new_guid, artist_name, artist_song, id_json,
                            data_json, image_json):
    """
    Add metadata for music video
    """
    self.db_cursor.execute('insert into mm_metadata_music_video (mm_metadata_music_video_guid,'
                           ' mm_metadata_music_video_media_id, mm_media_music_video_band,'
                           ' mm_media_music_video_song, mm_metadata_music_video_json,'
                           ' mm_metadata_music_video_localimage_json)'
                           ' values (%s,%s,%s,%s,%s,%s)',
                           (new_guid, id_json, artist_name, artist_song, data_json, image_json))
    self.db_commit()
    return new_guid


def db_meta_music_video_detail_uuid(self, item_guid):
    """
    Grab metadata for specififed music video
    """
    self.db_cursor.execute('select mm_media_music_video_band, mm_media_music_video_song,'
                           ' mm_metadata_music_video_json,'
                           ' mm_metadata_music_video_localimage_json'
                           ' from mm_metadata_music_video'
                           ' where mm_metadata_music_video_guid = %s', (item_guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_meta_music_video_count(self, imvdb_id=None, search_value=None):
    """
    Return count of music video metadata
    """
    if imvdb_id is None:
        if search_value is not None:
            self.db_cursor.execute('select count(*) from mm_metadata_music_video'
                                   ' where mm_media_music_video_song %% %s', (search_value,))
        else:
            self.db_cursor.execute(
                'select count(*) from mm_metadata_music_video')
    else:
        self.db_cursor.execute('select count(*) from mm_metadata_music_video'
                               ' where mm_metadata_music_video_media_id->\'imvdb\' ? %s',
                               (imvdb_id,))
    return self.db_cursor.fetchone()[0]


def db_meta_music_video_list(self, offset=0, records=None, search_value=None):
    """
    List music video metadata
    """
    # TODO order by release date
    if search_value is not None:
        self.db_cursor.execute('select mm_metadata_music_video_guid,'
                               ' mm_media_music_video_band, mm_media_music_video_song,'
                               ' mm_metadata_music_video_localimage_json'
                               ' from mm_metadata_music_video'
                               ' where mm_media_music_video_song %% %s '
                               'order by mm_media_music_video_band, mm_media_music_video_song'
                               ' offset %s limit %s',
                               (search_value, offset, records))
    else:
        self.db_cursor.execute('select mm_metadata_music_video_guid,'
                               ' mm_media_music_video_band, mm_media_music_video_song,'
                               ' mm_metadata_music_video_localimage_json'
                               ' from mm_metadata_music_video'
                               ' order by mm_media_music_video_band,'
                               ' mm_media_music_video_song offset %s limit %s',
                               (offset, records))
    return self.db_cursor.fetchall()
