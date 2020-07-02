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
import time

import requests
import tmdbsimple as tmdb
# TODO creates loop?  from metadata import metadata_movie
from tmdbv3api import Movie
from tmdbv3api import TMDb, TV

from . import common_global
from . import common_metadata
from . import common_network


class CommonMetadataTMDB:
    """
    Class for interfacing with TMDB
    """

    def __init__(self, option_config_json):
        self.API_KEY = option_config_json['API']['themoviedb']
        self.tmdbv3 = TMDb()
        self.tmdbv3.api_key = self.API_KEY
        tmdb.API_KEY = self.API_KEY
        self.movie = Movie()
        self.tv = TV()

    def com_tmdb_search(self, media_title, media_year=None, id_only=False, media_type='movie'):
        """
        # search for media title and year
        """
        common_global.es_inst.com_elastic_index('info', {"tmdb search": media_title,
                                                         'year': media_year})
        if media_type == 'movie':
            try:
                search = self.movie.search(media_title.replace('\\u25ba', ''))
            except:
                search = self.movie.search(media_title.encode('utf-8'))
        else:  # defaulting to TV search then
            try:
                search = self.tv.search(media_title.replace('\\u25ba', ''))
            except:
                search = self.tv.search(media_title.encode('utf-8'))
        common_global.es_inst.com_elastic_index('info', {'search': str(search)})
        if len(search) > 0:
            for res in search:
                # print(res.id, flush=True)
                # print(res.title, flush=True)
                # print(res.overview, flush=True)
                # print(res.poster_path, flush=True)
                # print(res.vote_average, flush=True)
                common_global.es_inst.com_elastic_index('info', {"result": res.title, 'id': res.id,
                                                                 'date':
                                                                     res.release_date.split('-', 1)[
                                                                         0]})
                if media_year is not None and type(media_year) is not list \
                        and (str(media_year) == res.release_date.split('-', 1)[0]
                             or str(int(media_year) - 1) == res.release_date.split('-', 1)[0]
                             or str(int(media_year) - 2) == res.release_date.split('-', 1)[0]
                             or str(int(media_year) - 3) == res.release_date.split('-', 1)[0]
                             or str(int(media_year) + 1) == res.release_date.split('-', 1)[0]
                             or str(int(media_year) + 2) == res.release_date.split('-', 1)[0]
                             or str(int(media_year) + 3) == res.release_date.split('-', 1)[0]):
                    if not id_only:
                        return 'info', self.com_tmdb_metadata_by_id(res.id)
                    else:
                        return 'idonly', res.id  # , s['title']
            return None, None
            # TODO multimatch......handle better!
            # TODO so, returning None, None for now
            # return 're', search.results
        else:
            return None, None

    def com_tmdb_metadata_by_id(self, tmdb_id):
        """
        Fetch all metadata by id to reduce calls
        """
        if tmdb_id[0:2].lower() == 'tt':
            # imdb_id......so, run find and then do the requests
            tmdb_id = metadata_movie_imdb.com_imdb_id_search(tmdb_id[0:2])
        try:
            return requests.get('https://api.themoviedb.org/3/movie/%s'
                                '?api_key=%s&append_to_response=credits,reviews,release_dates,videos' %
                                (tmdb_id, self.API_KEY))
        except requests.exceptions.ConnectionError:
            time.sleep(20)
            self.com_tmdb_metadata_by_id(tmdb_id)

    def com_tmdb_metadata_tv_by_id(self, tmdb_id):
        """
        Fetch all metadata by id to reduce calls
        """
        try:
            return requests.get('https://api.themoviedb.org/3/tv/%s'
                                '?api_key=%s&append_to_response=credits,reviews,release_dates,videos' %
                                (tmdb_id, self.API_KEY))
        except requests.exceptions.ConnectionError:
            time.sleep(20)
            self.com_tmdb_metadata_tv_by_id(tmdb_id)

    def com_tmdb_metadata_bio_by_id(self, tmdb_id):
        """
        Fetch all metadata bio by id to reduce calls
        """
        try:
            return requests.get('https://api.themoviedb.org/3/person/%s'
                                '?api_key=%s&append_to_response=combined_credits,external_ids,images' %
                                (tmdb_id, self.API_KEY))
        except requests.exceptions.ConnectionError:
            time.sleep(20)
            self.com_tmdb_metadata_bio_by_id(tmdb_id)

    def com_tmdb_meta_bio_image_build(self, result_json):
        """
        # download info and set data to be ready for insert into database
        """
        # common_global.es_inst.com_elastic_index('info', {'tmdb bio build': result_json})
        # create file path for poster
        image_file_path = common_metadata.com_meta_image_file_path(result_json['name'],
                                                                   'person')
        # common_global.es_inst.com_elastic_index('info', {'tmdb bio image path': image_file_path})
        if 'profile_path' in result_json and result_json['profile_path'] is not None:
            if not os.path.isfile(image_file_path + result_json['profile_path']):
                if result_json['profile_path'] is not None:
                    if not os.path.isfile(image_file_path):
                        common_network.mk_network_fetch_from_url(
                            'https://image.tmdb.org/t/p/original' + result_json['profile_path'],
                            image_file_path + result_json['profile_path'])
        # set local image json
        return ({'Images': {'themoviedb': image_file_path}})

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

    def com_tmdb_meta_by_id(self, tmdb_id):
        """
        # movie info by tmdb
        """
        movie = tmdb.Movies(tmdb_id)
        try:
            metadata = movie.info()
        except Exception as err_code:
            common_global.es_inst.com_elastic_index('error', {"TMDB Fetch Error": str(err_code)})
            metadata = None
        return metadata

    def com_tmdb_meta_cast_by_id(self, tmdb_id):
        """
        # cast by tmdb
        """
        movie = tmdb.Movies(tmdb_id)
        try:
            metadata = movie.credits()
        except Exception as err_code:
            common_global.es_inst.com_elastic_index('error', {"TMDB Fetch Credits Error":
                                                                  str(err_code)})
            metadata = None
        return metadata

    def com_tmdb_meta_review_by_id(self, tmdb_id):
        """
        # review by tmdb
        """
        movie = tmdb.Movies(tmdb_id)
        try:
            metadata = movie.reviews()
        except Exception as err_code:
            common_global.es_inst.com_elastic_index('error', {"TMDB Fetch Review Error": str(
                err_code)})
            metadata = None
        return metadata

    def com_tmdb_meta_release_by_id(self, tmdb_id):
        """
        # release by tmdb
        """
        movie = tmdb.Movies(tmdb_id)
        try:
            metadata = movie.releases()
        except Exception as err_code:
            common_global.es_inst.com_elastic_index('error',
                                                    {"TMDB Fetch Releases Error": str(err_code)})
            metadata = None
        return metadata

    # TODO
    # The supported external sources for each object are as follows:
    #    Movies: imdb_id
    #    People: imdb_id, freebase_mid, freebase_id
    #    TV Series: imdb_id, freebase_mid, freebase_id, tvdb_id
    #    TV Seasons: freebase_mid, freebase_id, tvdb_id
    #    TV Episodes: imdb_id, freebase_mid, freebase_id, tvdb_id

    def com_tmdb_meta_by_imdb_id(self, imdb_id):
        """
        # search by imdb
        """
        movie = tmdb.Find(imdb_id)
        try:
            metadata = movie.info(external_source='imdb_id')
        except Exception as err_code:
            common_global.es_inst.com_elastic_index('error',
                                                    {"TMDB Fetch imdb Error": str(err_code)})
            metadata = None
        return metadata

    def com_tmdb_meta_changes_movie(self):
        """
        # movie changes since date within 24 hours
        """
        changes = tmdb.Changes()
        movie_changes = changes.movie()
        return movie_changes

    def com_tmdb_meta_changes_tv(self):
        """
        # tv changes since date within 24 hours
        """
        changes = tmdb.Changes()
        tv_changes = changes.tv()
        return tv_changes

    def com_tmdb_meta_changes_person(self):
        """
        # person changes since date within 24 hours
        """
        changes = tmdb.Changes()
        person_changes = changes.person()
        return person_changes

    def com_tmdb_meta_collection_by_id(self, tmdb_id):
        """
        # collection info
        """
        movie_collection = tmdb.Collections(tmdb_id)
        try:
            metadata = movie_collection.info()
        except Exception as err_code:
            common_global.es_inst.com_elastic_index('error',
                                                    {"TMDB Fetch Collection Error": str(err_code)})
            metadata = None
        return metadata

    def com_tmdb_meta_info_build(self, result_json):
        """
        # download info and set data to be ready for insert into database
        """
        # common_global.es_inst.com_elastic_index('info', {'tmdb info build': result_json})
        # create file path for poster
        if 'title' in result_json:  # movie
            image_file_path = common_metadata.com_meta_image_file_path(result_json['title'],
                                                                       'poster')
        else:  # tv
            image_file_path = common_metadata.com_meta_image_file_path(result_json['name'],
                                                                       'poster')
        # common_global.es_inst.com_elastic_index('info', {'tmdb image path': image_file_path})
        poster_file_path = None
        if result_json['poster_path'] is not None:
            image_file_path += result_json['poster_path']
            if not os.path.isfile(image_file_path):
                common_network.mk_network_fetch_from_url('https://image.tmdb.org/t/p/original'
                                                         + result_json['poster_path'],
                                                         image_file_path)
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
                common_network.mk_network_fetch_from_url('https://image.tmdb.org/t/p/original'
                                                         + result_json['backdrop_path'],
                                                         image_file_path)
            backdrop_file_path = image_file_path
        # its a number so make it a string just in case
        if 'imdb_id' in result_json:  # in movies only
            series_id_json = json.dumps({'imdb': result_json['imdb_id'],
                                         'themoviedb': str(result_json['id'])})
        else:
            series_id_json = json.dumps({'themoviedb': str(result_json['id'])})
        # set local image json
        image_json = ({'Images': {'themoviedb': {'Backdrop': backdrop_file_path,
                                                 'Poster': poster_file_path}}})
        return series_id_json, result_json, image_json
