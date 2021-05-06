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

import asyncio
import inspect
import json
import os
import time

import httpx
from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_metadata
from common import common_network_async
from common import common_string
from guessit import guessit


class CommonMetadataTMDB:
    """
    Class for interfacing with TMDB
    """

    def __init__(self, option_config_json):
        self.API_KEY = option_config_json['API']['themoviedb']

    async def com_tmdb_search(self, media_title, media_year=None, id_only=True,
                              media_type=common_global.DLMediaType.Movie.value):
        """
        # search for media title and year
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        if media_type == common_global.DLMediaType.Movie.value:
            async with httpx.AsyncClient() as client:
                search_json = await client.get('https://api.themoviedb.org/3/search/movie'
                                               '?api_key=%s&include_adult=1&query=%s'
                                               % (self.API_KEY, media_title.encode('utf-8')),
                                               timeout=3.05)
        elif media_type == common_global.DLMediaType.TV.value:
            async with httpx.AsyncClient() as client:
                search_json = await client.get('https://api.themoviedb.org/3/search/tv'
                                               '?api_key=%s&include_adult=1&query=%s'
                                               % (self.API_KEY, media_title.encode('utf-8')),
                                               timeout=3.05)
        elif media_type == common_global.DLMediaType.Person.value:
            async with httpx.AsyncClient() as client:
                search_json = await client.get('https://api.themoviedb.org/3/search/person'
                                               '?api_key=%s&include_adult=1&query=%s'
                                               % (self.API_KEY, media_title.encode('utf-8')),
                                               timeout=3.05)
        else:  # invalid search type
            return None, None
        # pull json since it's a coroutine above
        search_json = search_json.json()
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'search': str(
                                                                                 search_json)})
        if search_json is not None and search_json['total_results'] > 0:
            for res in search_json['results']:
                await common_logging_elasticsearch_httpx.com_es_httpx_post_async(
                    message_type='info',
                    message_text={
                        "result": res['title'],
                        'id': res['id'],
                        'date':
                            res[
                                'release_date'].split(
                                '-',
                                1)[
                                0]})
                if media_year is not None and type(media_year) is not list \
                        and (str(media_year) == res['release_date'].split('-', 1)[0]
                             or str(int(media_year) - 1) == res['release_date'].split('-', 1)[0]
                             or str(int(media_year) - 2) == res['release_date'].split('-', 1)[0]
                             or str(int(media_year) - 3) == res['release_date'].split('-', 1)[0]
                             or str(int(media_year) + 1) == res['release_date'].split('-', 1)[0]
                             or str(int(media_year) + 2) == res['release_date'].split('-', 1)[0]
                             or str(int(media_year) + 3) == res['release_date'].split('-', 1)[0]):
                    if not id_only:
                        return 'info', self.com_tmdb_metadata_by_id(res['id'])
                    else:
                        return 'idonly', res['id']
            return None, None
        else:
            return None, None

    async def com_tmdb_metadata_by_id(self, tmdb_id):
        """
        Fetch all metadata by id to reduce calls
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        async with httpx.AsyncClient() as client:
            try:
                return await client.get('https://api.themoviedb.org/3/movie/%s'
                                        '?api_key=%s&append_to_response=credits,'
                                        'reviews,release_dates,videos' %
                                        (tmdb_id, self.API_KEY), timeout=3.05)
            except httpx.RequestError as exc:
                await common_logging_elasticsearch_httpx.com_es_httpx_post_async(
                    message_type='error',
                    message_text=
                    {
                        "TMDB Req com_tmdb_metadata_by_id":
                            str(exc)})
            except httpx.HTTPStatusError as exc:
                await common_logging_elasticsearch_httpx.com_es_httpx_post_async(
                    message_type='error',
                    message_text=
                    {
                        "TMDB Stat com_tmdb_metadata_by_id":
                            str(exc)})

    async def com_tmdb_metadata_tv_by_id(self, tmdb_id):
        """
        Fetch all metadata by id to reduce calls
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        async with httpx.AsyncClient() as client:
            try:
                return await client.get('https://api.themoviedb.org/3/tv/%s'
                                        '?api_key=%s&append_to_response=credits,'
                                        'reviews,release_dates,videos' %
                                        (tmdb_id, self.API_KEY), timeout=3.05)
            except httpx.RequestError as exc:
                await common_logging_elasticsearch_httpx.com_es_httpx_post_async(
                    message_type='error',
                    message_text=
                    {
                        "TMDB Req com_tmdb_metadata_tv_by_id":
                            str(exc)})
            except httpx.HTTPStatusError as exc:
                await common_logging_elasticsearch_httpx.com_es_httpx_post_async(
                    message_type='error',
                    message_text=
                    {
                        "TMDB Stat com_tmdb_metadata_tv_by_id":
                            str(exc)})

    async def com_tmdb_metadata_bio_by_id(self, tmdb_id):
        """
        Fetch all metadata bio by id to reduce calls
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        async with httpx.AsyncClient() as client:
            try:
                return await client.get('https://api.themoviedb.org/3/person/%s'
                                        '?api_key=%s&append_to_response=combined_credits,'
                                        'external_ids,images' %
                                        (tmdb_id, self.API_KEY), timeout=3.05)
            except httpx.RequestError as exc:
                await common_logging_elasticsearch_httpx.com_es_httpx_post_async(
                    message_type='error',
                    message_text=
                    {
                        "TMDB Req com_tmdb_metadata_bio_by_id":
                            str(exc)})
            except httpx.HTTPStatusError as exc:
                await common_logging_elasticsearch_httpx.com_es_httpx_post_async(
                    message_type='error',
                    message_text=
                    {
                        "TMDB Stat com_tmdb_metadata_bio_by_id":
                            str(exc)})

    async def com_tmdb_meta_bio_image_build(self, result_json):
        """
        # download info and set data to be ready for insert into database
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        # create file path for poster
        image_file_path = await common_metadata.com_meta_image_file_path(result_json['name'],
                                                                         'person')
        if 'profile_path' in result_json and result_json['profile_path'] is not None:
            if not os.path.isfile(image_file_path + result_json['profile_path']):
                if result_json['profile_path'] is not None:
                    if not os.path.isfile(image_file_path):
                        await common_network_async.mk_network_fetch_from_url_async(
                            'https://image.tmdb.org/t/p/original' + result_json['profile_path'],
                            image_file_path + result_json['profile_path'])
        # set local image json
        return image_file_path.replace(common_global.static_data_directory, '')

    async def com_tmdb_metadata_id_max(self):
        """
        Grab high metadata id
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        return json.loads(await common_network_async.mk_network_fetch_from_url_async(
            'https://api.themoviedb.org/3/movie/latest'
            '?api_key=%s' % self.API_KEY))['id']

    async def com_tmdb_metadata_bio_id_max(self):
        """
        Grab high bios metadata id (person)
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        return json.loads(await common_network_async.mk_network_fetch_from_url_async(
            'https://api.themoviedb.org/3/person/latest'
            '?api_key=%s' % self.API_KEY))['id']

    async def com_tmdb_metadata_tv_id_max(self):
        """
        Grab high tv metadata id
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        return json.loads(await common_network_async.mk_network_fetch_from_url_async(
            'https://api.themoviedb.org/3/tv/latest'
            '?api_key=%s' % self.API_KEY))['id']

    async def com_tmdb_meta_review_by_id(self, tmdb_id):
        """
        # review by tmdb
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        return json.loads(await common_network_async.mk_network_fetch_from_url_async(
            'https://api.themoviedb.org/3/review/%s'
            '?api_key=%s', (self.API_KEY, tmdb_id)))

    async def com_tmdb_meta_changes_person(self):
        """
        # person changes since date within 24 hours
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        return json.loads(await common_network_async.mk_network_fetch_from_url_async(
            'https://api.themoviedb.org/3/person/changes'
            '?api_key=%s' % self.API_KEY))['id']

    async def com_tmdb_meta_collection_by_id(self, tmdb_id):
        """
        # collection info
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        return json.loads(await common_network_async.mk_network_fetch_from_url_async(
            'https://api.themoviedb.org/3/collection/%s'
            '?api_key=%s', (self.API_KEY, tmdb_id)))

    async def com_tmdb_meta_info_build(self, result_json):
        """
        # download info and set data to be ready for insert into database
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        # create file path for poster
        if 'title' in result_json:  # movie
            image_file_path = await common_metadata.com_meta_image_file_path(result_json['title'],
                                                                             'poster')
        else:  # tv
            image_file_path = await common_metadata.com_meta_image_file_path(result_json['name'],
                                                                             'poster')
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'tmdb image path':
                                                                                 image_file_path})
        poster_file_path = None
        if result_json['poster_path'] is not None:
            image_file_path += result_json['poster_path']
            if not os.path.isfile(image_file_path):
                if await common_network_async.mk_network_fetch_from_url_async(
                        'https://image.tmdb.org/t/p/original'
                        + result_json['poster_path'],
                        image_file_path):
                    pass  # download is successful
                else:
                    image_file_path = None
            poster_file_path = image_file_path
        # create file path for backdrop
        if 'title' in result_json:  # movie
            image_file_path = await common_metadata.com_meta_image_file_path(result_json['title'],
                                                                             'backdrop')
        else:  # tv
            image_file_path = await common_metadata.com_meta_image_file_path(result_json['name'],
                                                                             'backdrop')
        backdrop_file_path = None
        if result_json['backdrop_path'] is not None:
            image_file_path += result_json['backdrop_path']
            if not os.path.isfile(image_file_path):
                if await common_network_async.mk_network_fetch_from_url_async(
                        'https://image.tmdb.org/t/p/original'
                        + result_json['backdrop_path'],
                        image_file_path):
                    pass  # download is successful
                else:
                    image_file_path = None
            backdrop_file_path = image_file_path
        # set local image json
        if poster_file_path is not None:
            poster_file_path = poster_file_path.replace(common_global.static_data_directory, '')
        if backdrop_file_path is not None:
            backdrop_file_path = backdrop_file_path.replace(common_global.static_data_directory, '')
        image_json = (
            {'Backdrop': backdrop_file_path,
             'Poster': poster_file_path})
        return result_json['id'], result_json, image_json


async def movie_search_tmdb(db_connection, file_name):
    """
    # search tmdb
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    # TODO aren't I doing two guessits per file name then?
    file_name = guessit(file_name)
    if type(file_name['title']) == list:
        file_name['title'] = common_string.com_string_guessit_list(file_name['title'])
    metadata_uuid = None
    # try to match ID ONLY
    if 'year' in file_name:
        match_response, match_result = await common_global.api_instance.com_tmdb_search(
            file_name['title'], file_name['year'], id_only=True,
            media_type=common_global.DLMediaType.Movie.value)
    else:
        match_response, match_result = await common_global.api_instance.com_tmdb_search(
            file_name['title'], None, id_only=True,
            media_type=common_global.DLMediaType.Movie.value)
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         "meta movie response":
                                                                             match_response,
                                                                         'res': match_result})
    if match_response == 'idonly':
        # check to see if metadata exists for TMDB id
        metadata_uuid = await db_connection.db_meta_guid_by_tmdb(match_result)
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             "meta movie db result": metadata_uuid})
    elif match_response == 'info':
        # store new metadata record and set uuid
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             "meta movie movielookup info "
                                                                             "results": match_result})
    elif match_response == 're':
        # multiple results
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             "movielookup multiple results":
                                                                                 match_result})
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'meta movie uuid': metadata_uuid,
                                                                         'result': match_result})
    return metadata_uuid, match_result


async def movie_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid):
    """
    # fetch from tmdb
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    # fetch and save json data via tmdb id
    result_json = await common_global.api_instance.com_tmdb_metadata_by_id(tmdb_id)
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         "meta fetch result": result_json})
    if result_json is not None:
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             "meta movie code": result_json.status_code,
                                                                             "header": result_json.headers})
        # 504	Your request to the backend server timed out. Try again.
        if result_json.status_code == 504:
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 "meta movie tmdb 504": tmdb_id})
            await asyncio.sleep(60)
            # redo fetch due to 504
            await movie_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid)
        elif result_json.status_code == 200:
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 "meta movie save fetch result":
                                                                                     result_json.json()})
            series_id_json, result_json, image_json \
                = await common_global.api_instance.com_tmdb_meta_info_build(result_json.json())
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 "series": series_id_json})
            # set and insert the record if doesn't exist
            if await db_connection.db_meta_movie_guid_count(metadata_uuid) == 0:
                await db_connection.db_meta_insert_tmdb(metadata_uuid,
                                                        series_id_json,
                                                        result_json['title'],
                                                        json.dumps(result_json),
                                                        json.dumps(image_json))
                # under guid check as don't need to insert them if already exist
                if 'credits' in result_json:  # cast/crew doesn't exist on all media
                    if 'cast' in result_json['credits']:
                        await db_connection.db_meta_person_insert_cast_crew('themoviedb',
                                                                            result_json['credits'][
                                                                                'cast'])
                    if 'crew' in result_json['credits']:
                        await db_connection.db_meta_person_insert_cast_crew('themoviedb',
                                                                            result_json['credits'][
                                                                                'crew'])
        # 429	Your request count (#) is over the allowed limit of (40).
        elif result_json.status_code == 429:
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 "meta movie tmdb 429": tmdb_id})
            await asyncio.sleep(30)
            # redo fetch due to 429
            await movie_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid)
        elif result_json.status_code == 404:
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 "meta movie tmdb 404": tmdb_id})
            # TODO handle 404's better
            metadata_uuid = None
    else:  # is this is None....
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             "meta movie tmdb misc": tmdb_id})
        metadata_uuid = None
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'meta movie save fetch return uuid':
                                                                             metadata_uuid})
    return metadata_uuid


async def movie_fetch_save_tmdb_review(db_connection, tmdb_id):
    """
    # grab reviews
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    review_json = await common_global.api_instance.com_tmdb_meta_review_by_id(tmdb_id)
    # review record doesn't exist on all media
    if review_json is not None and review_json['total_results'] > 0:
        review_json_id = ({'themoviedb': str(review_json['id'])})
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             "review": review_json_id})
        await db_connection.db_review_insert(json.dumps(review_json_id),
                                             json.dumps({'themoviedb': review_json}))


async def movie_fetch_save_tmdb_collection(db_connection, tmdb_collection_id, download_data):
    """
    # grab collection
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    # store/update the record
    # don't string this since it's a pure result store
    collection_guid = await db_connection.db_collection_by_tmdb(tmdb_collection_id)
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         "collection": tmdb_collection_id,
                                                                         'guid': collection_guid})
    if collection_guid is None:
        # insert
        collection_meta = await common_global.api_instance.com_tmdb_meta_collection_by_id(
            tmdb_collection_id)
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             "col": collection_meta})
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
        await db_connection.db_collection_insert(download_data['Name'], download_data['GUID'],
                                                 collection_meta, {'Poster': image_poster_path,
                                                                   'Backdrop': image_backdrop_path})
        # commit all changes to db
        await db_connection.db_commit()
        return 1  # to add totals later
    else:
        # update
        # db_connection.db_collection_update(collection_guid, guid_list)
        return 0  # to add totals later


async def metadata_fetch_tmdb_person(db_connection, provider_name, download_data):
    """
    fetch person bio
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if common_global.api_instance is not None:
        # fetch and save json data via tmdb id
        result_json = await common_global.api_instance.com_tmdb_metadata_bio_by_id(
            download_data['mdq_download_json']['ProviderMetaID'])
        if result_json is None or result_json.status_code == 502:
            await asyncio.sleep(60)
            await metadata_fetch_tmdb_person(db_connection, provider_name, download_data)
        elif result_json.status_code == 200:
            await db_connection.db_meta_person_update(provider_name=provider_name,
                                                      provider_uuid=
                                                      int(download_data['mdq_download_json'][
                                                              'ProviderMetaID']),
                                                      person_bio=result_json.json(),
                                                      person_image=await common_global.api_instance.com_tmdb_meta_bio_image_build(
                                                          result_json.json()))
            await db_connection.db_download_delete(download_data['mdq_id'])
            await db_connection.db_commit()
