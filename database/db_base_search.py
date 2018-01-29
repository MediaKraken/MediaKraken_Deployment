'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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
import logging  # pylint: disable=W0611
import json


def db_search(self, search_string, search_type='Local'):
    """
    search media local, remote and metadata providers
    """
    json_return_data = {}
    if search_type == 'Local':
        # movie section
        self.db_cursor.execute('SELECT mm_metadata_guid, mm_media_name, ' \
                               'similarity(mm_media_name, %s) AS sml' \
                               ' FROM mm_metadata_movie WHERE mm_media_name % %s' \
                               ' ORDER BY sml DESC, mm_media_name;',
                               (search_string, search_string))
        json_return_data['Movie': json.dumps(self.db_cursor.fetchall())]
        # tv show section
        self.db_cursor.execute('SELECT mm_metadata_tvshow_guid, mm_metadata_tvshow_name,' \
                               ' similarity(mm_metadata_tvshow_name, %s) AS sml' \
                               ' FROM mm_metadata_tvshow WHERE mm_metadata_tvshow_name % %s' \
                               ' ORDER BY sml DESC, mm_metadata_tvshow_name;',
                               (search_string, search_string))
        json_return_data['TVShow': json.dumps(self.db_cursor.fetchall())]
        # album section
        self.db_cursor.execute('SELECT mm_metadata_album_guid, mm_metadata_album_name,' \
                               ' similarity(mm_metadata_album_name, %s) AS sml' \
                               ' FROM mm_metadata_album WHERE mm_metadata_album_name % %s' \
                               ' ORDER BY sml DESC, mm_metadata_album_name;',
                               (search_string, search_string))
        json_return_data['Album': json.dumps(self.db_cursor.fetchall())]
    return json_return_data
