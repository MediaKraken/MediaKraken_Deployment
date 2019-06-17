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


def db_music_video_list_count(self, search_value=None):
    """
    Music video count
    """
    if search_value is not None:
        self.db_cursor.execute('select count(*) from mm_metadata_music_video, mm_media'
                               ' where mm_media_metadata_guid = mm_metadata_music_video_guid group'
                               ' and mm_media_music_video_song %% %s', (search_value,))
    else:
        self.db_cursor.execute('select count(*) from mm_metadata_music_video, mm_media'
                               ' where mm_media_metadata_guid = mm_metadata_music_video_guid')
    return self.db_cursor.fetchone()[0]


def db_music_video_list(self, offset=0, per_page=None, search_value=None):
    """
    music video list
    """
    pass
