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
import logging # pylint: disable=W0611
import uuid
import json


def db_meta_anime_title_insert(self, ani_media_id_json, ani_name, ani_json,\
                               ani_image_local, ani_user_json):
    """
    Insert new anidb entries into database
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_metadata_anime(mm_metadata_anime_guid,'\
        ' mm_metadata_anime_media_id, mm_media_anime_name, mm_metadata_anime_json,'\
        ' mm_metadata_anime_localimage_json, mm_metadata_anime_user_json)\
        values (%s,%s,%s,%s,%s,%s)', (new_guid, ani_media_id_json, ani_name, ani_json,\
                                      ani_image_local, ani_user_json))
    self.db_commit()
    return new_guid


def db_meta_anime_title_search(self, title_to_search):
    """
    search for title
    """
    # TODO hit movie and tv db's as well?
    self.db_cursor.execute('select mm_metadata_anime_guid from mm_metadata_anime'\
        ' where mm_media_anime_name = %s', (title_to_search,))
    try:
        return self.db_cursor.fetchone()[0]
    except:
        return None


def db_meta_anime_update_meta_id(self, media_id_json):
    """
    Update the media id json from scudlee data
    """
    logging.debug('ani_id_json %s', media_id_json)
    self.db_cursor.execute('update mm_metadata_anime set mm_metadata_anime_media_id = %s'\
                           ' where mm_metadata_anime_media_id->\'anidb\' ? %s',\
                           (media_id_json, json.loads(media_id_json)['anidb']))
    self.db_commit()
