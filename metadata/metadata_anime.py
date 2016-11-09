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
from guessit import guessit
from common import common_config_ini
from common import common_metadata_anidb


option_config_json, db_connection = common_config_ini.com_config_read()


# verify provider key exists
if option_config_json['API']['AniDB'] is not None:
    # setup the connection class
    ANIDB_CONNECTION = common_metadata_anidb.CommonMetadataANIdb(option_config_json)
else:
    ANIDB_CONNECTION = None


def metadata_anime_lookup(db_connection, file_name, download_que_id):
    """
    Check for anime in tv sections of the metadata providers
    """
    if not hasattr(metadata_anime_lookup, "metadata_last_id"):
        metadata_anime_lookup.metadata_last_id = None # it doesn't exist yet, so initialize it
        metadata_anime_lookup.metadata_last_title = None
        metadata_anime_lookup.metadata_last_year = None
        metadata_anime_lookup.metadata_last_imdb = None
        metadata_anime_lookup.metadata_last_tmdb = None
        metadata_anime_lookup.metadata_last_rt = None
        metadata_anime_lookup.metadata_last_anidb = None
    metadata_uuid = None # so not found checks verify later
    logging.info('meta anime look filename: %s', file_name)
    # check for dupes by name/year
    if 'year' in file_name:
        if file_name['title'] == metadata_anime_lookup.metadata_last_title\
                and file_name['year'] == metadata_anime_lookup.metadata_last_year:
            db_connection.db_download_delete(download_que_id)
            logging.info('meta movie return 1 %s',  metadata_anime_lookup.metadata_last_id)
            # don't need to set last......since they are equal
            return metadata_anime_lookup.metadata_last_id
    elif file_name['title'] == metadata_anime_lookup.metadata_last_title:
        db_connection.db_download_delete(download_que_id)
        logging.info('meta movie return 2 %s',  metadata_anime_lookup.metadata_last_id)
        # don't need to set last......since they are equal
        return metadata_anime_lookup.metadata_last_id


# themoviedb 
# tvmaze
# thetvdb
# anidb




    # set last values to negate lookups for same title/show
    metadata_anime_lookup.metadata_last_id = metadata_uuid
    metadata_anime_lookup.metadata_last_title = file_name['title']
    try:
        metadata_anime_lookup.metadata_last_year = file_name['year']
    except:
        metadata_anime_lookup.metadata_last_year = None
    metadata_anime_lookup.metadata_last_imdb = imdb_id
    metadata_anime_lookup.metadata_last_tmdb = tmdb_id
    metadata_anime_lookup.metadata_last_rt = rt_id
    metadata_anime_lookup.metadata_last_anidb = anidb
    return metadata_uuid
