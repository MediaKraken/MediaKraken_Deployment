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


def db_metathesportsdb_select_guid(self, guid):
    """
    # select
    """
    self.db_cursor.execute('select mm_metadata_sports_json'
                           ' from mm_metadata_sports'
                           ' where mm_metadata_sports_guid = %s', (guid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_sports_json']
    except:
        return None


def db_metathesportsdb_insert(self, series_id_json, event_name, show_detail,
                              image_json):
    """
    # insert
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_metadata_sports (mm_metadata_sports_guid,'
                           ' mm_metadata_media_sports_id,'
                           ' mm_metadata_sports_name,'
                           ' mm_metadata_sports_json,'
                           ' mm_metadata_sports_image_json)'
                           ' values (%s,%s,%s,%s,%s)',
                           (new_guid, series_id_json, event_name, show_detail, image_json))
    self.db_commit()
    return new_guid


def db_metathesports_update(self, series_id_json, event_name, show_detail,
                            sportsdb_id):
    """
    # updated
    """
    self.db_cursor.execute('update mm_metadata_sports'
                           ' set mm_metadata_media_sports_id = %s,'
                           ' mm_metadata_sports_name = %s,'
                           ' mm_metadata_sports_json = %s'
                           ' where mm_metadata_media_sports_id->\'thesportsdb\' ? %s',
                           (series_id_json, event_name, show_detail, sportsdb_id))
    self.db_commit()
