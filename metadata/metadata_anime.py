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
import logging # pylint: disable=W0611
import sys
sys.path.append("./common")
from guessit import guessit


def metadata_anime_lookup(db_connection, media_file_path, download_que_id):
    """
    Check for anime in tv sections of the metadata providers
    """
    metadata_uuid, imdb_id, tmdb_id = nfo_xml_db_lookup_tv(db_connection, nfo_data, xml_data)
    if metadata_uuid is None:
        metadata_uuid = tveps_lookup(guessit(media_file_path), imdb_id, tvdb_id, 'en')
    if metadata_uuid is None:
        # check movie data
        metadata_uuid, imdb_id, tmdb_id = nfo_xml_db_lookup(db_connection, nfo_data, xml_data)
        if metadata_uuid is None:
            metadata_uuid = movie_lookup(guessit(media_file_path), imdb_id, tmdb_id)
    # TODO   or perhaps JMM hit
    # TODO   hit anidb
    return metadata_uuid
