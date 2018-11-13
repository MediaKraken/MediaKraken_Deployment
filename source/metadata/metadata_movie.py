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

import json
import time

from common import common_config_ini
from common import common_global
from common import common_metadata
from common import common_metadata_tmdb
from common import common_string
from guessit import guessit

from . import metadata_nfo_xml

option_config_json, db_connection = common_config_ini.com_config_read()

# verify themoviedb key exists
if option_config_json['API']['themoviedb'] is not None:
    # setup the thmdb class
    TMDB_CONNECTION = common_metadata_tmdb.CommonMetadataTMDB(
        option_config_json)
else:
    TMDB_CONNECTION = None


def movie_search_tmdb(db_connection, file_name):
    """
    # search tmdb
    """
    try:
        common_global.es_inst.com_elastic_index('info', {"meta movie search tmdb": str(file_name)})
    except:
        pass
    file_name = guessit(file_name)
    if type(file_name['title']) == list:
        file_name['title'] = common_string.com_string_guessit_list(file_name['title'])
    metadata_uuid = None
    match_result = None
    if TMDB_CONNECTION is not None:
        # try to match ID ONLY
        if 'year' in file_name:
            match_response, match_result = TMDB_CONNECTION.com_tmdb_search(
                file_name['title'], file_name['year'], True)
        else:
            match_response, match_result = TMDB_CONNECTION.com_tmdb_search(
                file_name['title'], None, True)
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
    result_json = TMDB_CONNECTION.com_tmdb_metadata_by_id(tmdb_id)
    common_global.es_inst.com_elastic_index('info', {"meta movie code": result_json.status_code})
    if result_json.status_code == 200:
        common_global.es_inst.com_elastic_index('info', {"meta movie save fetch result":
                                                             result_json.json()})
        series_id_json, result_json, image_json \
            = TMDB_CONNECTION.com_tmdb_meta_info_build(result_json.json())
        # set and insert the record
        meta_json = ({'Meta': {'themoviedb': {'Meta': result_json}}})
        common_global.es_inst.com_elastic_index('info', {"series": series_id_json})
        # set and insert the record
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
    elif result_json.status_code == 502:
        time.sleep(300)
        # redo fetch due to 502
        movie_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid)
    elif result_json.status_code == 404:
        # TODO handle 404's better
        metadata_uuid = None
    else:  # is this is None....
        metadata_uuid = None
    common_global.es_inst.com_elastic_index('info', {'meta movie save fetch uuid':
                                                         metadata_uuid})
    return metadata_uuid


def movie_fetch_tmdb_imdb(imdb_id):
    """
    # fetch from tmdb via imdb
    """
    result_json = TMDB_CONNECTION.com_tmdb_meta_by_imdb_id(imdb_id)
    common_global.es_inst.com_elastic_index('info', {"uhimdb": result_json})
    if result_json is not None:
        try:
            return result_json['movie_results'][0]['id']
        except:
            return None
    else:
        return None


def movie_fetch_save_tmdb_cast_crew(db_connection, tmdb_id, metadata_id):
    """
    Save cast/crew
    """
    cast_json = TMDB_CONNECTION.com_tmdb_meta_cast_by_id(tmdb_id)
    if cast_json is not None:  # cast/crew doesn't exist on all media
        if 'cast' in cast_json:
            # verify the person is not already in the database
            if db_connection.db_meta_person_id_count('themoviedb', cast_json['cast']) == 0:
                # TODO must verify a fetch record doesn't exist already
                db_connection.db_meta_person_insert_cast_crew(
                    'themoviedb', cast_json['cast'])
        if 'crew' in cast_json:
            # verify the person is not already in the database
            if db_connection.db_meta_person_id_count('themoviedb', cast_json['cast']) == 0:
                # TODO must verify a fetch record doesn't exist already
                db_connection.db_meta_person_insert_cast_crew(
                    'themoviedb', cast_json['crew'])
        # update the metadata record with the cast info
        db_connection.db_meta_movie_update_castcrew(cast_json, metadata_id)


def movie_fetch_save_tmdb_review(db_connection, tmdb_id):
    """
    # grab reviews
    """
    review_json = TMDB_CONNECTION.com_tmdb_meta_review_by_id(tmdb_id)
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
        collection_meta = TMDB_CONNECTION.com_tmdb_meta_collection_by_id(
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
        localimage_json = {'Poster': image_poster_path,
                           'Backdrop': image_backdrop_path}
        db_connection.db_collection_insert(download_data['Name'], download_data['GUID'],
                                           collection_meta, localimage_json)
        # commit all changes to db
        db_connection.db_commit()
        return 1  # to add totals later
    else:
        # update
        # db_connection.db_collection_update(collection_guid, guid_list)
        return 0  # to add totals later


def metadata_movie_lookup(db_connection, media_file_path, download_que_json, download_que_id,
                          file_name):
    """
    Movie lookup
    This is the main function called from metadata_identification
    """
    # don't bother checking title/year as the main_server_metadata_api_worker does it already
    if not hasattr(metadata_movie_lookup, "metadata_last_id"):
        # it doesn't exist yet, so initialize it
        metadata_movie_lookup.metadata_last_id = None
        metadata_movie_lookup.metadata_last_imdb = None
        metadata_movie_lookup.metadata_last_tmdb = None
        metadata_movie_lookup.metadata_last_rt = None
    metadata_uuid = None  # so not found checks verify later
    common_global.es_inst.com_elastic_index('info', {'metadata_movie_lookup': str(file_name)})
    # determine provider id's from nfo/xml if they exist
    nfo_data, xml_data = metadata_nfo_xml.nfo_xml_file(media_file_path)
    imdb_id, tmdb_id, rt_id = metadata_nfo_xml.nfo_xml_id_lookup(nfo_data, xml_data)
    if imdb_id is not None or tmdb_id is not None or rt_id is not None:
        common_global.es_inst.com_elastic_index('info', {"meta movie look": imdb_id,
                                                         'tmdb': tmdb_id,
                                                         'rt': rt_id})
    # if same as last, return last id and save lookup
    if imdb_id is not None and imdb_id == metadata_movie_lookup.metadata_last_imdb:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_movie_lookup.metadata_last_id
    if tmdb_id is not None and tmdb_id == metadata_movie_lookup.metadata_last_tmdb:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_movie_lookup.metadata_last_id
    if rt_id is not None and rt_id == metadata_movie_lookup.metadata_last_rt:
        db_connection.db_download_delete(download_que_id)
        # don't need to set last......since they are equal
        return metadata_movie_lookup.metadata_last_id
    # doesn't match last id's so continue lookup
    # if ids from nfo/xml, query local db to see if exist
    if tmdb_id is not None:
        metadata_uuid = db_connection.db_meta_guid_by_tmdb(tmdb_id)
    if imdb_id is not None and metadata_uuid is None:
        metadata_uuid = db_connection.db_meta_guid_by_imdb(imdb_id)
    if rt_id is not None and metadata_uuid is None:
        metadata_uuid = db_connection.db_meta_guid_by_rt(rt_id)
    # if ids from nfo/xml on local db
    common_global.es_inst.com_elastic_index('info', {"meta movie metadata_uuid A": metadata_uuid})
    if metadata_uuid is not None:
        db_connection.db_download_delete(download_que_id)
        # fall through here to set last id's
    else:
        # check to see if id is known from nfo/xml but not in db yet so fetch data
        if tmdb_id is not None or imdb_id is not None:
            if tmdb_id is not None:
                provider_id = str(tmdb_id)
            else:
                provider_id = imdb_id
            dl_meta = db_connection.db_download_que_exists(download_que_id, 0, 'themoviedb',
                                                           provider_id)
            if dl_meta is None:
                metadata_uuid = download_que_json['MetaNewID']
                download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': provider_id})
                db_connection.db_download_update(json.dumps(download_que_json),
                                                 download_que_id)
                # set provider last so it's not picked up by the wrong thread too early
                db_connection.db_download_update_provider('themoviedb', download_que_id)
            else:
                db_connection.db_download_delete(download_que_id)
                metadata_uuid = dl_meta
    common_global.es_inst.com_elastic_index('info', {"meta movie metadata_uuid B": metadata_uuid})
    if metadata_uuid is None:
        # no ids found on the local database so begin name/year searches
        common_global.es_inst.com_elastic_index('info', {'stuff': "meta movie db lookup"})
        # db lookup by name and year (if available)
        if 'year' in file_name:
            metadata_uuid = db_connection.db_find_metadata_guid(file_name['title'],
                                                                file_name['year'])
        else:
            metadata_uuid = db_connection.db_find_metadata_guid(file_name['title'], None)
        common_global.es_inst.com_elastic_index('info', {"meta movie db meta": metadata_uuid})
        if metadata_uuid is not None:
            # match found by title/year on local db so purge dl record
            db_connection.db_download_delete(download_que_id)
        else:
            # no matches by name/year on local database
            # search themoviedb since not matched above via DB or nfo/xml
            download_que_json.update({'Status': 'Search'})
            # save the updated status
            db_connection.db_download_update(json.dumps(download_que_json),
                                             download_que_id)
            # set provider last so it's not picked up by the wrong thread
            db_connection.db_download_update_provider('themoviedb', download_que_id)
    common_global.es_inst.com_elastic_index('info', {"metadata_movie return uuid": metadata_uuid})
    # set last values to negate lookups for same title/show
    metadata_movie_lookup.metadata_last_id = metadata_uuid
    metadata_movie_lookup.metadata_last_imdb = imdb_id
    metadata_movie_lookup.metadata_last_tmdb = tmdb_id
    metadata_movie_lookup.metadata_last_rt = rt_id
    return metadata_uuid
