'''
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
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import re
import os
import json
import MK_Common_Metadata
import com_network
import tmdbsimple as tmdb


class CommonMetadataTMDB(object):
    """
    Class for interfacing with TMDB
    """
    def __init__(self):
        # pull in the ini file config
        import ConfigParser
        Config = ConfigParser.ConfigParser()
        if os.path.exists("MediaKraken.ini"):
            Config.read("MediaKraken.ini")
        else:
            Config.read("../../MediaKraken_Server/MediaKraken.ini")
        tmdb.API_KEY = Config.get('API', 'theMovieDB').strip()


    # search for movie title and year
    def MK_Common_TMDB_Search(self, movie_title, movie_year=None, id_only=False):
        logging.debug("tmdb search %s %s", movie_title, movie_year)
        search = tmdb.Search()
        response = search.movie(query=movie_title)
        for s in search.results:
            logging.debug("result: %s %s %s", s['title'], s['id'],\
                s['release_date'].split('-', 1)[0])
            # TODO   this should be year =, up and down
            if movie_year is not None and (str(movie_year) == s['release_date'].split('-', 1)[0]
                        or str(int(movie_year) - 1) == s['release_date'].split('-', 1)[0]
                        or str(int(movie_year) + 1) == s['release_date'].split('-', 1)[0]):
                if not id_only:
                    return 'info', MK_Common_TMDB_Metadata_By_ID(s['id'])
                else:
                    return 'idonly', s['id'] #, s['title']
        return 're', search.results


    # search by tmdb
    def MK_Common_TMDB_Metadata_By_ID(self, tmdb_id):
        movie = tmdb.Movies(tmdb_id)
        try:
            metadata = movie.info()
        except Exception as e:
            logging.error("TMDB Fetch Error: %s" % str(e))
            metadata = None
        return metadata


    # search by tmdb
    def MK_Common_TMDB_Metadata_Cast_By_ID(self, tmdb_id):
        movie = tmdb.Movies(tmdb_id)
        try:
            metadata = movie.credits()
        except Exception as e:
            logging.error("TMDB Fetch Credits Error: %s" % str(e))
            metadata = None
        return metadata


    # review by tmdb
    def MK_Common_TMDB_Metadata_Review_By_ID(self, tmdb_id):
        movie = tmdb.Movies(tmdb_id)
        try:
            metadata = movie.reviews()
        except Exception as e:
            logging.error("TMDB Fetch Review Error: %s" % str(e))
            metadata = None
        return metadata


# TODO
#The supported external sources for each object are as follows:
#    Movies: imdb_id
#    People: imdb_id, freebase_mid, freebase_id, tvrage_id
#    TV Series: imdb_id, freebase_mid, freebase_id, tvdb_id, tvrage_id
#    TV Seasons: freebase_mid, freebase_id, tvdb_id, tvrage_id
#    TV Episodes: imdb_id, freebase_mid, freebase_id, tvdb_id, tvrage_id


    # search by imdb
    def MK_Common_TMDB_Metadata_By_IMDB_ID(self, imdb_id):
        movie = tmdb.Find(imdb_id)
        try:
            metadata = movie.info(external_source='imdb_id')
        except Exception as e:
            logging.error("TMDB Fetch IMDB Error: %s" % str(e))
            metadata = None
        return metadata


    # movie changes since date within 24 hours
    def MK_Common_TMDB_Metadata_Changes_Movie(self):
        changes = tmdb.Changes()
        movie_changes = changes.movie()
        return movie_changes


    # tv changes since date within 24 hours
    def MK_Common_TMDB_Metadata_Changes_TV(self):
        changes = tmdb.Changes()
        tv_changes = changes.tv()
        return tv_changes


    # person changes since date within 24 hours
    def MK_Common_TMDB_Metadata_Changes_Person(self):
        changes = tmdb.Changes()
        person_changes = changes.person()
        return person_changes


    # collection info
    def MK_Common_TMDB_Metadata_Collection_By_ID(self, tmdb_id):
        movie_collection = tmdb.Collections(tmdb_id)
        try:
            metadata = movie_collection.info()
        except Exception as e:
            logging.error("TMDB Fetch Collection Error: %s" % str(e))
            metadata = None
        return metadata


    # download info and set data to be ready for insert into database
    def MK_Common_TMDB_MetaData_Info_Build(self, result_json):
        logging.debug('tmdb info build: %s', result_json)
        # create file path for poster
        file_path = MK_Common_Metadata.MK_Common_Metadata_Image_File_Path(result_json['title'],\
            'poster')
        poster_file_path = None
        if result_json['poster_path'] is not None:
            file_path += result_json['poster_path']
            if not os.path.isfile(file_path):
                com_network.MK_Network_Fetch_From_URL('https://image.tmdb.org/t/p/original'\
                    + result_json['poster_path'], file_path)
            poster_file_path = file_path
        # create file path for backdrop
        file_path = MK_Common_Metadata.MK_Common_Metadata_Image_File_Path(result_json['title'],\
            'backdrop')
        backdrop_file_path = None
        if result_json['backdrop_path'] is not None:
            file_path += result_json['backdrop_path']
            if not os.path.isfile(file_path):
                com_network.MK_Network_Fetch_From_URL('https://image.tmdb.org/t/p/original'\
                    + result_json['backdrop_path'], file_path)
            backdrop_file_path = file_path
        # its a number so make it a string just in case
        series_id_json = json.dumps({'IMDB':result_json['imdb_id'], 'TMDB':str(result_json['id'])})
        # set local image json
        image_json = ({'Images': {'TMDB':{'Backdrop':backdrop_file_path,\
            'Poster':poster_file_path}}})
        #result_json.update({'LocalImages':{'Backdrop':backdrop_file_path, 'Poster':poster_file_path}})
        return series_id_json, result_json, image_json
