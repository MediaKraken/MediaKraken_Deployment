"""
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
"""

import json


def db_search(self, search_string, search_type='Local', search_movie=True, search_tvshow=True,
              search_album=True, search_image=True, search_publication=True, search_game=True):
    """
    search media local, remote and metadata providers
    """
    json_return_data = {}
    if search_type == 'Local':
        if search_movie:
            # movie section
            self.db_cursor.execute('SELECT mm_metadata_guid, mm_media_name, '
                                   'similarity(mm_media_name, %s) AS sml'
                                   ' FROM mm_metadata_movie WHERE mm_media_name % %s'
                                   ' ORDER BY sml DESC, mm_media_name;',
                                   (search_string, search_string))
            json_return_data['Movie': json.dumps(self.db_cursor.fetchall())]
        if search_tvshow:
            # tv show section
            self.db_cursor.execute('SELECT mm_metadata_tvshow_guid, mm_metadata_tvshow_name,'
                                   ' similarity(mm_metadata_tvshow_name, %s) AS sml'
                                   ' FROM mm_metadata_tvshow WHERE mm_metadata_tvshow_name % %s'
                                   ' ORDER BY sml DESC, mm_metadata_tvshow_name;',
                                   (search_string, search_string))
            json_return_data['TVShow': json.dumps(self.db_cursor.fetchall())]
        if search_album:
            # album section
            self.db_cursor.execute('SELECT mm_metadata_album_guid, mm_metadata_album_name,'
                                   ' similarity(mm_metadata_album_name, %s) AS sml'
                                   ' FROM mm_metadata_album WHERE mm_metadata_album_name % %s'
                                   ' ORDER BY sml DESC, mm_metadata_album_name;',
                                   (search_string, search_string))
            json_return_data['Album': json.dumps(self.db_cursor.fetchall())]
        if search_image:
            # TODO image search
            pass
        if search_publication:
            # publication section
            self.db_cursor.execute('SELECT mm_metadata_book_guid, mm_metadata_book_name,'
                                   ' similarity(mm_metadata_book_name, %s) AS sml'
                                   ' FROM mm_metadata_book WHERE mm_metadata_book_name % %s'
                                   ' ORDER BY sml DESC, mm_metadata_book_name;',
                                   (search_string, search_string))
            json_return_data['Publication': json.dumps(self.db_cursor.fetchall())]
        if search_game:
            # game section
            self.db_cursor.execute('SELECT gi_id, gi_game_info_name,'
                                   ' similarity(gi_game_info_name, %s) AS sml'
                                   ' FROM mm_metadata_game_software_info'
                                   ' WHERE gi_game_info_name % %s'
                                   ' ORDER BY sml DESC, gi_game_info_name;',
                                   (search_string, search_string))
            json_return_data['Game': json.dumps(self.db_cursor.fetchall())]
    return json_return_data
