"""
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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
import os

import httpx

from . import common_global
from . import common_metadata
from . import common_network


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
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {"tmdb search": media_title,
                                                         'year': media_year})
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
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'search': str(search_json)})
        if search_json is not None and search_json['total_results'] > 0:
            for res in search_json['results']:
                common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {"result": res['title'],
                                                                 'id': res['id'],
                                                                 'date':
                                                                     res['release_date'].split('-',
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
        async with httpx.AsyncClient() as client:
            try:
                return await client.get('https://api.themoviedb.org/3/movie/%s'
                                        '?api_key=%s&append_to_response=credits,'
                                        'reviews,release_dates,videos' %
                                        (tmdb_id, self.API_KEY), timeout=3.05)
            except httpx.RequestError as exc:
                common_global.es_inst.com_elastic_index('error',
                                                        {"TMDB Req com_tmdb_metadata_by_id":
                                                             str(exc)})
            except httpx.HTTPStatusError as exc:
                common_global.es_inst.com_elastic_index('error',
                                                        {"TMDB Stat com_tmdb_metadata_by_id":
                                                             str(exc)})

    async def com_tmdb_metadata_tv_by_id(self, tmdb_id):
        """
        Fetch all metadata by id to reduce calls
        """
        async with httpx.AsyncClient() as client:
            try:
                return await client.get('https://api.themoviedb.org/3/tv/%s'
                                        '?api_key=%s&append_to_response=credits,'
                                        'reviews,release_dates,videos' %
                                        (tmdb_id, self.API_KEY), timeout=3.05)
            except httpx.RequestError as exc:
                common_global.es_inst.com_elastic_index('error',
                                                        {"TMDB Req com_tmdb_metadata_tv_by_id":
                                                             str(exc)})
            except httpx.HTTPStatusError as exc:
                common_global.es_inst.com_elastic_index('error',
                                                        {"TMDB Stat com_tmdb_metadata_tv_by_id":
                                                             str(exc)})

    async def com_tmdb_metadata_bio_by_id(self, tmdb_id):
        """
        Fetch all metadata bio by id to reduce calls
        """
        async with httpx.AsyncClient() as client:
            try:
                return await client.get('https://api.themoviedb.org/3/person/%s'
                                        '?api_key=%s&append_to_response=combined_credits,'
                                        'external_ids,images' %
                                        (tmdb_id, self.API_KEY), timeout=3.05)
            except httpx.RequestError as exc:
                common_global.es_inst.com_elastic_index('error',
                                                        {"TMDB Req com_tmdb_metadata_bio_by_id":
                                                             str(exc)})
            except httpx.HTTPStatusError as exc:
                common_global.es_inst.com_elastic_index('error',
                                                        {"TMDB Stat com_tmdb_metadata_bio_by_id":
                                                             str(exc)})

    def com_tmdb_meta_bio_image_build(self, result_json):
        """
        # download info and set data to be ready for insert into database
        """
        # create file path for poster
        image_file_path = common_metadata.com_meta_image_file_path(result_json['name'],
                                                                   'person')
        if 'profile_path' in result_json and result_json['profile_path'] is not None:
            if not os.path.isfile(image_file_path + result_json['profile_path']):
                if result_json['profile_path'] is not None:
                    if not os.path.isfile(image_file_path):
                        common_network.mk_network_fetch_from_url(
                            'https://image.tmdb.org/t/p/original' + result_json['profile_path'],
                            image_file_path + result_json['profile_path'])
        # set local image json
        return image_file_path.replace(common_global.static_data_directory, '')

    def com_tmdb_metadata_id_max(self):
        """
        Grab high metadata id
        """
        return json.loads(common_network.mk_network_fetch_from_url(
            'https://api.themoviedb.org/3/movie/latest'
            '?api_key=%s' % self.API_KEY))['id']

    def com_tmdb_metadata_bio_id_max(self):
        """
        Grab high bios metadata id (person)
        """
        return json.loads(common_network.mk_network_fetch_from_url(
            'https://api.themoviedb.org/3/person/latest'
            '?api_key=%s' % self.API_KEY))['id']

    def com_tmdb_metadata_tv_id_max(self):
        """
        Grab high tv metadata id
        """
        return json.loads(common_network.mk_network_fetch_from_url(
            'https://api.themoviedb.org/3/tv/latest'
            '?api_key=%s' % self.API_KEY))['id']

    def com_tmdb_meta_review_by_id(self, tmdb_id):
        """
        # review by tmdb
        """
        return json.loads(common_network.mk_network_fetch_from_url(
            'https://api.themoviedb.org/3/review/%s'
            '?api_key=%s', (self.API_KEY, tmdb_id)))

    def com_tmdb_meta_changes_movie(self):
        """
        # movie changes since date within 24 hours
        """
        return json.loads(common_network.mk_network_fetch_from_url(
            'https://api.themoviedb.org/3/movie/changes'
            '?api_key=%s' % self.API_KEY))['id']

    def com_tmdb_meta_changes_tv(self):
        """
        # tv changes since date within 24 hours
        """
        return json.loads(common_network.mk_network_fetch_from_url(
            'https://api.themoviedb.org/3/tv/changes'
            '?api_key=%s' % self.API_KEY))['id']

    def com_tmdb_meta_changes_person(self):
        """
        # person changes since date within 24 hours
        """
        return json.loads(common_network.mk_network_fetch_from_url(
            'https://api.themoviedb.org/3/person/changes'
            '?api_key=%s' % self.API_KEY))['id']

    def com_tmdb_meta_collection_by_id(self, tmdb_id):
        """
        # collection info
        """
        return json.loads(common_network.mk_network_fetch_from_url(
            'https://api.themoviedb.org/3/collection/%s'
            '?api_key=%s', (self.API_KEY, tmdb_id)))

    def com_tmdb_meta_info_build(self, result_json):
        """
        # download info and set data to be ready for insert into database
        """
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'tmdb info build': result_json})
        # create file path for poster
        if 'title' in result_json:  # movie
            image_file_path = common_metadata.com_meta_image_file_path(result_json['title'],
                                                                       'poster')
        else:  # tv
            image_file_path = common_metadata.com_meta_image_file_path(result_json['name'],
                                                                       'poster')
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'tmdb image path': image_file_path})
        poster_file_path = None
        if result_json['poster_path'] is not None:
            image_file_path += result_json['poster_path']
            if not os.path.isfile(image_file_path):
                if common_network.mk_network_fetch_from_url('https://image.tmdb.org/t/p/original'
                                                            + result_json['poster_path'],
                                                            image_file_path):
                    pass  # download is successful
                else:
                    image_file_path = None
            poster_file_path = image_file_path
        # create file path for backdrop
        if 'title' in result_json:  # movie
            image_file_path = common_metadata.com_meta_image_file_path(result_json['title'],
                                                                       'backdrop')
        else:  # tv
            image_file_path = common_metadata.com_meta_image_file_path(result_json['name'],
                                                                       'backdrop')
        backdrop_file_path = None
        if result_json['backdrop_path'] is not None:
            image_file_path += result_json['backdrop_path']
            if not os.path.isfile(image_file_path):
                if common_network.mk_network_fetch_from_url('https://image.tmdb.org/t/p/original'
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
