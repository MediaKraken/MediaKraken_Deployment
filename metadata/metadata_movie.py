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
import json
from guessit import guessit
from common import common_config_ini
from common import common_metadata_anidb
from common import common_metadata_imdb
from common import common_metadata_movie_theme
from common import common_metadata_movie_trailer
from common import common_metadata_netflixroulette
from common import common_metadata_omdb
from common import common_metadata_tmdb
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()
from . import metadata_nfo_xml


# verify themovietb key exists
if option_config_json['API']['theMovieDB'] is not None:
    # setup the thmdb class
    TMDB_CONNECTION = common_metadata_tmdb.CommonMetadataTMDB(option_config_json)
else:
    TMDB_CONNECTION = None


def movie_search_tmdb(db_connection, file_name):
    """
    # search tmdb
    """
    logging.debug("search tmdb: %s", file_name)
    file_name = guessit(file_name)
    metadata_uuid = None
    if TMDB_CONNECTION is not None:
        # try to match ID ONLY
        if 'year' in file_name:
            match_response, match_result = TMDB_CONNECTION.com_tmdb_search(\
                file_name['title'], file_name['year'], True)
        else:
            match_response, match_result = TMDB_CONNECTION.com_tmdb_search(\
                file_name['title'], None, True)
        logging.debug("response: %s %s", match_response, match_result)
        if match_response == 'idonly':
            # check to see if metadata exists for TMDB id
            metadata_uuid = db_connection.db_meta_guid_by_tmdb(match_result)
            logging.debug("db result: %s", metadata_uuid)
        elif match_response == 'info':
            # store new metadata record and set uuid
            logging.info("movielookup info results: %s", match_result)
        elif match_response == 're':
            # multiple results
            logging.info("movielookup multiple results: %s", match_result)
    return metadata_uuid, match_result


def movie_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid):
    """
    # fetch from tmdb
    """
    logging.debug("tmdb fetch: %s", tmdb_id)
    # fetch and save json data via tmdb id
    result_json = TMDB_CONNECTION.com_tmdb_meta_by_id(tmdb_id)
    logging.debug("uh: %s", result_json)
    if result_json is not None:
        series_id_json, result_json, image_json\
            = TMDB_CONNECTION.com_tmdb_meta_info_build(result_json)
        # set and insert the record
        meta_json = ({'Meta': {'TMDB': {'Meta': result_json, 'Cast': None, 'Crew': None}}})
        logging.debug("series: %s", series_id_json)
        # set and insert the record
        db_connection.db_meta_insert_tmdb(metadata_uuid, series_id_json,\
            result_json['title'], json.dumps(meta_json), json.dumps(image_json))
    else:
        metadata_uuid = None
    return metadata_uuid


def movie_fetch_tmdb_imdb(imdb_id):
    """
    # fetch from tmdb via imdb
    """
    result_json = TMDB_CONNECTION.com_tmdb_meta_by_imdb_id(imdb_id)
    logging.debug("uhimdb: %s", result_json)
    if result_json is not None:
        # find call for tmdb returns the other sections
        # {u'tv_season_results': [], u'tv_episode_results': [], u'person_results': [],\
        # u'tv_results': [], u'movie_results': []}
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
    if 'cast' in cast_json:
        db_connection.db_meta_person_insert_cast_crew('TMDB', cast_json['cast'])
    if 'crew' in cast_json:
        db_connection.db_meta_person_insert_cast_crew('TMDB', cast_json['crew'])
    # update the metadata record with the cast info
    db_connection.db_meta_movie_update_castcrew(tmdb_id, cast_json, metadata_id)


def movie_fetch_save_tmdb_review(db_connection, tmdb_id):
    """
    # grab reviews
    """
    review_json = TMDB_CONNECTION.com_tmdb_meta_review_by_id(tmdb_id)
    if review_json['total_results'] > 0:
        review_json_id = ({'TMDB': str(review_json['id'])})
        logging.debug("review: %s", review_json_id)
        db_connection.db_review_insert(json.dumps(review_json_id),\
            json.dumps({'TMDB': review_json}))


def metadata_movie_lookup(db_connection, media_file_path, download_que_json, download_que_id):
    """
    Movie lookup
    This is the main function called from metadata_identification
    """
    if not hasattr(metadata_movie_lookup, "metadata_last_id"):
        metadata_movie_lookup.metadata_last_id = None # it doesn't exist yet, so initialize it
        metadata_movie_lookup.metadata_last_title = None
        metadata_movie_lookup.metadata_last_year = None
        metadata_movie_lookup.metadata_last_imdb = None
        metadata_movie_lookup.metadata_last_tmdb = None
        metadata_movie_lookup.metadata_last_rt = None
    # determine file name/etc for handling name/year skips
    file_name = guessit(media_file_path)
    logging.debug('movielook filename: %s', file_name)
    # check for dupes by name/year
    if 'year' in file_name:
        if file_name['title'] == metadata_movie_lookup.metadata_last_title\
                and file_name['year'] == metadata_movie_lookup.metadata_last_year:
            db_connection.db_download_delete(download_que_id)
            return metadata_movie_lookup.metadata_last_id
    elif file_name['title'] == metadata_movie_lookup.metadata_last_title:
        db_connection.db_download_delete(download_que_id)
        return metadata_movie_lookup.metadata_last_id
    # determine provider id's from nfo/xml if they exist
    imdb_id, tmdb_id, rt_id = metadata_nfo_xml.nfo_xml_id_lookup(\
        metadata_nfo_xml.nfo_xml_file(media_file_path))
    logging.debug("movie look: %s %s %s %s %s %s", imdb_id, tmdb_id, rt_id,\
        metadata_movie_lookup.metadata_last_imdb, metadata_movie_lookup.metadata_last_tmdb,\
        metadata_movie_lookup.metadata_last_rt)
    # if same as last, return last id and save lookup
    if imdb_id is not None and imdb_id == metadata_movie_lookup.metadata_last_imdb:
        return metadata_movie_lookup.metadata_last_id
    if tmdb_id is not None and tmdb_id == metadata_movie_lookup.metadata_last_tmdb:
        return metadata_movie_lookup.metadata_last_id
    if rt_id is not None and rt_id == metadata_movie_lookup.metadata_last_rt:
        return metadata_movie_lookup.metadata_last_id
    # if ids from nfo/xml, query local db to see if exist
    if tmdb_id is not None:
        metadata_uuid = db_connection.db_meta_guid_by_tmdb(tmdb_id)
    if imdb_id is not None and metadata_uuid is None:
        metadata_uuid = db_connection.db_meta_guid_by_imdb(imdb_id)
    if rt_id is not None and metadata_uuid is None:
        metadata_uuid = db_connection.db_meta_guid_by_rt(rt_id)
    # if ids from nfo/xml on local db
    if metadata_uuid is not None:
        db_connection.db_download_delete(download_que_id)
        return metadata_uuid
    else:
        # id is known from nfo/xml but not in db yet so fetch data
        if tmdb_id is not None or imdb_id is not None:
            if tmdb_id is not None:
                dl_meta = db_connection.db_download_que_exists('themoviedb', str(tmdb_id))
                if dl_meta is None:
                    download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': str(tmdb_id)})
                    db_connection.db_download_update(json.dumps(download_que_json),\
                        download_que_id)
                    # set provider last so it's not picked up by the wrong thread too early
                    db_connection.db_download_update_provider('themoviedb', download_que_id)
                else:
                    db_connection.db_download_delete(download_que_id)
                    metadata_uuid = dl_meta
            else:
                dl_meta = db_connection.db_download_que_exists('themoviedb', imdb_id)
                if dl_meta is None:
                    download_que_json.update({'Status': 'Fetch', 'ProviderMetaID': imdb_id})
                    db_connection.db_download_update(json.dumps(download_que_json),\
                        download_que_id)
                    # set provider last so it's not picked up by the wrong thread too early
                    db_connection.db_download_update_provider('themoviedb', download_que_id)
                else:
                    db_connection.db_download_delete(download_que_id)
                    metadata_uuid = dl_meta
    if metadata_uuid is None:
        # no ids found on the local database so begin name/year searches
        logging.debug("movie db lookup")
        # db lookup by name and year (if available)
        if 'year' in file_name:
            metadata_uuid = db_connection.db_find_metadata_guid(file_name['title'],\
                file_name['year'])
        else:
            metadata_uuid = db_connection.db_find_metadata_guid(file_name['title'], None)
        logging.debug("movie db meta: %s", metadata_uuid)
        if metadata_uuid is not None:
            # match found by title/year on local db so purge dl record
            db_connection.db_download_delete(download_que_id)
        else:
            # no matches by name/year
            # search themoviedb since not matched above via DB or nfo/xml
            download_que_json.update({'Status': 'Search'})
            # save the updated status
            db_connection.db_download_update(json.dumps(download_que_json),\
                download_que_id)
            # set provider last so it's not picked up by the wrong thread
            db_connection.db_download_update_provider('themoviedb', download_que_id)
    # set last values to negate lookups for same title/show
    metadata_movie_lookup.metadata_last_id = metadata_uuid
    metadata_movie_lookup.metadata_last_title = file_name['title']
    try:
        metadata_movie_lookup.metadata_last_year = file_name['year']
    except:
        metadata_movie_lookup.metadata_last_year = None
    metadata_movie_lookup.metadata_last_imdb = imdb_id
    metadata_movie_lookup.metadata_last_tmdb = tmdb_id
    metadata_movie_lookup.metadata_last_rt = rt_id
    return metadata_uuid
