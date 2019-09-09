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

import time
import psycopg2
from common import common_config_ini
from common import common_global
from common import common_metadata_provider_musicbrainz


def music_search_musicbrainz(db_connection, file_name):
    """
    # search musicbrainz
    """
    try:
        common_global.es_inst.com_elastic_index('info',
                                                {"meta movie search musicbrainz": str(file_name)})
    except:
        pass


    # TODO aren't I doing two guessits per file name then?
    file_name = guessit(file_name)
    if type(file_name['title']) == list:
        file_name['title'] = common_string.com_string_guessit_list(file_name['title'])
    metadata_uuid = None
    # try to match ID ONLY
    if 'year' in file_name:
        match_response, match_result = TMDB_CONNECTION.com_tmdb_search(
            file_name['title'], file_name['year'], True, media_type='movie')
    else:
        match_response, match_result = TMDB_CONNECTION.com_tmdb_search(
            file_name['title'], None, True, media_type='movie')
    common_global.es_inst.com_elastic_index('info', {"meta movie response":
                                                         match_response, 'res': match_result})
    if match_response == 'idonly':
        # check to see if metadata exists for TMDB id
        metadata_uuid = db_connection.db_meta_guid_by_tmdb(match_result)
        common_global.es_inst.com_elastic_index('info', {"meta movie db result": metadata_uuid})
    elif match_response == 'info':
        # store new metadata record and set uuid
        common_global.es_inst.com_elastic_index('info', {"meta movie movielookup info "
                                                         "results": match_result})
    elif match_response == 're':
        # multiple results
        common_global.es_inst.com_elastic_index('info', {"movielookup multiple results":
                                                             match_result})
    common_global.es_inst.com_elastic_index('info', {'meta movie uuid': metadata_uuid,
                                                     'result': match_result})
    return metadata_uuid, match_result


def music_fetch_save_musicbrainz(db_connection, tmdb_id, metadata_uuid):
    """
    # fetch from musicbrainz
    """
    common_global.es_inst.com_elastic_index('info', {"meta movie tmdb save fetch": tmdb_id})
    # fetch and save json data via tmdb id
    result_json = TMDB_CONNECTION.com_tmdb_metadata_by_id(tmdb_id)
    if result_json is not None:
        common_global.es_inst.com_elastic_index('info', {"meta movie code": result_json.status_code,
                                                         "header": result_json.headers})
    # 504	Your request to the backend server timed out. Try again.
    if result_json is None or result_json.status_code == 504:
        time.sleep(60)
        # redo fetch due to 504
        movie_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid)
    elif result_json.status_code == 200:
        common_global.es_inst.com_elastic_index('info', {"meta movie save fetch result":
                                                             result_json.json()})
        series_id_json, result_json, image_json \
            = TMDB_CONNECTION.com_tmdb_meta_info_build(result_json.json())
        # set and insert the record
        meta_json = ({'Meta': {'themoviedb': {'Meta': result_json}}})
        common_global.es_inst.com_elastic_index('info', {"series": series_id_json})
        # set and insert the record
        try:
            db_connection.db_meta_insert_tmdb(metadata_uuid, series_id_json,
                                              result_json['title'], json.dumps(meta_json),
                                              json.dumps(image_json))
            if 'credits' in result_json:  # cast/crew doesn't exist on all media
                if 'cast' in result_json['credits']:
                    db_connection.db_meta_person_insert_cast_crew('themoviedb',
                                                                  result_json['credits']['cast'])
                if 'crew' in result_json['credits']:
                    db_connection.db_meta_person_insert_cast_crew('themoviedb',
                                                                  result_json['credits']['crew'])
        # this except is to check duplicate keys for mm_metadata_pk
        except psycopg2.IntegrityError:
            # TODO technically I could be missing cast/crew if the above doesn't finish after the insert
            pass
    # 429	Your request count (#) is over the allowed limit of (40).
    elif result_json.status_code == 429:
        time.sleep(10)
        # redo fetch due to 504
        movie_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid)
    elif result_json.status_code == 404:
        # TODO handle 404's better
        metadata_uuid = None
    else:  # is this is None....
        metadata_uuid = None
    common_global.es_inst.com_elastic_index('info', {'meta movie save fetch uuid':
                                                         metadata_uuid})
    return metadata_uuid
