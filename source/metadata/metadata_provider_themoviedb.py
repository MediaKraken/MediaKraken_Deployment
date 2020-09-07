"""
  Copyright (C) 2019 Quinn D Granfor <spootdev@gmail.com>

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
import time

from common import common_global
from common import common_metadata
from common import common_string
from guessit import guessit


def movie_search_tmdb(db_connection, file_name):
    """
    # search tmdb
    """
    common_global.es_inst.com_elastic_index('info', {"meta movie search tmdb": str(file_name)})
    # TODO aren't I doing two guessits per file name then?
    file_name = guessit(file_name)
    if type(file_name['title']) == list:
        file_name['title'] = common_string.com_string_guessit_list(file_name['title'])
    metadata_uuid = None
    # try to match ID ONLY
    if 'year' in file_name:
        match_response, match_result = common_global.api_instance.com_tmdb_search(
            file_name['title'], file_name['year'], id_only=True,
            media_type=common_global.DLMediaType.Movie.value)
    else:
        match_response, match_result = common_global.api_instance.com_tmdb_search(
            file_name['title'], None, id_only=True,
            media_type=common_global.DLMediaType.Movie.value)
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


def movie_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid):
    """
    # fetch from tmdb
    """
    common_global.es_inst.com_elastic_index('info', {"meta movie tmdb save fetch": tmdb_id})
    # fetch and save json data via tmdb id
    result_json = common_global.api_instance.com_tmdb_metadata_by_id(tmdb_id)
    common_global.es_inst.com_elastic_index('info', {"meta fetch result": result_json})
    if result_json is not None:
        common_global.es_inst.com_elastic_index('info', {"meta movie code": result_json.status_code,
                                                         "header": result_json.headers})
    # 504	Your request to the backend server timed out. Try again.
    if result_json.status_code == 504:
        common_global.es_inst.com_elastic_index('info', {"meta movie tmdb 504": tmdb_id})
        time.sleep(60)
        # redo fetch due to 504
        movie_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid)
    elif result_json.status_code == 200:
        common_global.es_inst.com_elastic_index('info', {"meta movie save fetch result":
                                                             result_json.json()})
        series_id_json, result_json, image_json \
            = common_global.api_instance.com_tmdb_meta_info_build(result_json.json())
        common_global.es_inst.com_elastic_index('info', {"series": series_id_json})
        # set and insert the record if doesn't exist
        if db_connection.db_meta_movie_guid_count(metadata_uuid) == 0:
            db_connection.db_meta_insert_tmdb(metadata_uuid,
                                              series_id_json,
                                              result_json['title'],
                                              json.dumps(result_json),
                                              json.dumps(image_json))
        if 'credits' in result_json:  # cast/crew doesn't exist on all media
            if 'cast' in result_json['credits']:
                db_connection.db_meta_person_insert_cast_crew('themoviedb',
                                                              result_json['credits']['cast'])
            if 'crew' in result_json['credits']:
                db_connection.db_meta_person_insert_cast_crew('themoviedb',
                                                              result_json['credits']['crew'])
    # 429	Your request count (#) is over the allowed limit of (40).
    elif result_json.status_code == 429:
        common_global.es_inst.com_elastic_index('info', {"meta movie tmdb 429": tmdb_id})
        time.sleep(30)
        # redo fetch due to 429
        movie_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid)
    elif result_json.status_code == 404:
        common_global.es_inst.com_elastic_index('info', {"meta movie tmdb 404": tmdb_id})
        # TODO handle 404's better
        metadata_uuid = None
    else:  # is this is None....
        common_global.es_inst.com_elastic_index('info', {"meta movie tmdb misc": tmdb_id})
        metadata_uuid = None
    common_global.es_inst.com_elastic_index('info', {'meta movie save fetch return uuid':
                                                         metadata_uuid})
    return metadata_uuid


def movie_fetch_save_tmdb_review(db_connection, tmdb_id):
    """
    # grab reviews
    """
    review_json = common_global.api_instance.com_tmdb_meta_review_by_id(tmdb_id)
    # review record doesn't exist on all media
    if review_json is not None and review_json['total_results'] > 0:
        review_json_id = ({'themoviedb': str(review_json['id'])})
        common_global.es_inst.com_elastic_index('info', {"review": review_json_id})
        db_connection.db_review_insert(json.dumps(review_json_id),
                                       json.dumps({'themoviedb': review_json}))


def movie_fetch_save_tmdb_collection(db_connection, tmdb_collection_id, download_data):
    """
    # grab collection
    """
    # store/update the record
    # don't string this since it's a pure result store
    collection_guid = db_connection.db_collection_by_tmdb(tmdb_collection_id)
    common_global.es_inst.com_elastic_index('info', {"collection": tmdb_collection_id,
                                                     'guid': collection_guid})
    if collection_guid is None:
        # insert
        collection_meta = common_global.api_instance.com_tmdb_meta_collection_by_id(
            tmdb_collection_id)
        common_global.es_inst.com_elastic_index('info', {"col": collection_meta})
        # poster path
        if download_data['Poster'] is not None:
            image_poster_path = common_metadata.com_meta_image_path(download_data['Name'],
                                                                    'poster', 'themoviedb',
                                                                    download_data['Poster'])
        else:
            image_poster_path = None
        # backdrop path
        if download_data['Backdrop'] is not None:
            image_backdrop_path = common_metadata.com_meta_image_path(download_data['Name'],
                                                                      'backdrop', 'themoviedb',
                                                                      download_data['Backdrop'])
        else:
            image_backdrop_path = None
        db_connection.db_collection_insert(download_data['Name'], download_data['GUID'],
                                           collection_meta, {'Poster': image_poster_path,
                                                             'Backdrop': image_backdrop_path})
        # commit all changes to db
        db_connection.db_commit()
        return 1  # to add totals later
    else:
        # update
        # db_connection.db_collection_update(collection_guid, guid_list)
        return 0  # to add totals later


def metadata_fetch_tmdb_person(thread_db, provider_name, download_data):
    """
    fetch person bio
    """
    if common_global.api_instance is not None:
        common_global.es_inst.com_elastic_index('info', {"meta person tmdb save fetch":
                                                             download_data})
        # fetch and save json data via tmdb id
        result_json = common_global.api_instance.com_tmdb_metadata_bio_by_id(
            download_data['mdq_download_json']['ProviderMetaID'])
        common_global.es_inst.com_elastic_index('info', {"meta person code":
                                                             result_json.status_code})
        common_global.es_inst.com_elastic_index('info', {"meta person save fetch result":
                                                             result_json.json()})
        if result_json is None or result_json.status_code == 502:
            time.sleep(60)
            metadata_fetch_tmdb_person(thread_db, provider_name, download_data)
        elif result_json.status_code == 200:
            thread_db.db_meta_person_update(provider_name,
                                            download_data['mdq_download_json']['ProviderMetaID'],
                                            result_json.json(),
                                            common_global.api_instance.com_tmdb_meta_bio_image_build(
                                                result_json.json()))
            # commit happens in download delete
            thread_db.db_download_delete(download_data['mdq_id'])
