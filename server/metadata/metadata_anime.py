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

import sys
sys.path.append("../MediaKraken_Common")
from guessit import guessit
import logging


def metadata_anime_lookup(db, media_file_path, download_que_id):
    # check tv show data
    metadata_uuid, imdb_id, tmdb_id = nfo_xml_db_lookup_tv(db, nfo_data, xml_data)
    if metadata_uuid is None:
        metadata_uuid = tveps_lookup(guessit(media_file_path), imdb_id, tvdb_id, 'en')
    if metadata_uuid is None:
        # check movie data
        metadata_uuid, imdb_id, tmdb_id = nfo_xml_db_lookup(db, nfo_data, xml_data)
        if metadata_uuid is None:
            metadata_uuid = movie_lookup(guessit(media_file_path), imdb_id, tmdb_id)
    # TODO   or perhaps JMM hit
    # TODO   hit anidb
    return metadata_uuid
