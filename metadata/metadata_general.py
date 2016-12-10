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
from common import common_metadata_tv_theme
from . import metadata_anime
from . import metadata_game
from . import metadata_movie
from . import metadata_music
from . import metadata_music_video
from . import metadata_periodicals
from . import metadata_person
from . import metadata_sports
from . import metadata_tv


def metadata_process(thread_db, provider_name, download_data):
    logging.info('full downloaddata record: %s', download_data)
    # TODO art, posters, trailers, etc in here as well
    if download_data['mdq_download_json']['Status'] == "Search":
        logging.info('%s search', provider_name)
        metadata_search(thread_db, provider_name, download_data)
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        logging.info('%s fetch %s', provider_name,\
                      download_data['mdq_download_json']['ProviderMetaID'])
        metadata_fetch(thread_db, provider_name, download_data)
    elif download_data['mdq_download_json']['Status'] == "FetchCastCrew":
        logging.info('%s fetchcastcrew', provider_name)
        metadata_castcrew(thread_db, provider_name, download_data)
    elif download_data['mdq_download_json']['Status'] == "FetchReview":
        logging.info('%s fetchreview', provider_name)
        metadata_review(thread_db, provider_name, download_data)
    elif download_data['mdq_download_json']['Status'] == "FetchImage":
        logging.info('%s fetchimage', provider_name)
        metadata_image(thread_db, provider_name, download_data)
    elif download_data['mdq_download_json']['Status'] == "FetchCollection":
        logging.info('%s fetchcollection', provider_name)
        metadata_collection(thread_db, provider_name, download_data)
    elif download_data['mdq_download_json']['Status'] == "FetchPersonBio":
        logging.info('%s fetch person bio', provider_name)
        metadata_person(thread_db, provider_name, download_data)


def metadata_search(thread_db, provider_name, download_data):
    """
    Search for metadata via specified provider
    """
    metadata_uuid = None
    match_result = None
    set_fetch = False
    lookup_halt = False
    update_provider = None
    if provider_name == 'imvdb':
        metadata_uuid, match_result = metadata_music_video.metadata_music_video_lookup()
        if metadata_uuid is None:
            if match_result is None:
                update_provider = 'theaudiodb'
            else:
                set_fetch = True
    elif provider_name == 'televisiontunes':
        # if download succeeds remove dl
        metadata_uuid = common_metadata_tv_theme.com_tvtheme_download(\
            guessit(download_data['Path'])['title'])
        if metadata_uuid is not None:
            # TODO add theme.mp3 dl'd above to media table
            thread_db.db_download_delete(download_data['mdq_id'])
            return # since it's a search/fetch/insert in one shot
        else:
            lookup_halt = True
    elif provider_name == 'themoviedb':
        metadata_uuid, match_result = metadata_movie.movie_search_tmdb(thread_db,\
            download_data['mdq_download_json']['Path'])
        logging.info('metadata_uuid %s, match_result %s', metadata_uuid, match_result)
        # if match_result is an int, that means the lookup found a match but isn't in db
        if metadata_uuid is None and type(match_result) != int:
            update_provider = 'omdb'
        else:
            if metadata_uuid is None:
                set_fetch = True
    elif provider_name == 'thetvdb':
        metadata_uuid, match_result =  metadata_tv.tv_search_tvdb(thread_db,\
            download_data['mdq_download_json']['Path'])
        if metadata_uuid is None:
            if match_result is None:
                lookup_halt = True
            else:
                set_fetch = True
    elif provider_name == 'tvmaze':
        metadata_uuid, match_result =  metadata_tv.tv_search_tvmaze(thread_db,\
            download_data['mdq_download_json']['Path'])
        if metadata_uuid is None:
            if match_result is None:
                update_provider = 'thetvdb'
            else:
                set_fetch = True
    elif provider_name == 'omdb':
        lookup_halt = True

    # if search is being updated to new provider
    if update_provider is not None:
        thread_db.db_download_update_provider(update_provider, download_data['mdq_id'])
        return # no need to continue with checks
    # if lookup halt set to ZZ so it doesn't get picked up my metadata dl ques
    if lookup_halt:
        thread_db.db_download_update_provider('ZZ', download_data['mdq_id'])
        return # no need to continue with checks
    # if set fetch, set provider id and status on dl record
    if set_fetch:
        # first verify a download que record doesn't exist for this id
        metadata_uuid = thread_db.db_download_que_exists(download_data['mdq_id'],\
            provider_name, str(match_result))
        logging.info('metaquelook: %s', metadata_uuid)
        if metadata_uuid is not None:
            thread_db.db_update_media_id(download_data['mdq_download_json']['MediaID'],\
                metadata_uuid)
            # found in database so remove from download que
            thread_db.db_download_delete(download_data['mdq_id'])
        else:
            metadata_uuid = download_data['mdq_download_json']['MetaNewID']
            logging.info('meta: %s', metadata_uuid)
            thread_db.db_update_media_id(download_data['mdq_download_json']['MediaID'],\
                                         download_data['mdq_download_json']['MetaNewID'])
            logging.info('after media id')
            download_data['mdq_download_json'].update({'ProviderMetaID': str(match_result)})
            download_data['mdq_download_json'].update({'Status': 'Fetch'})
            logging.info('after json update')
            thread_db.db_download_update(json.dumps(download_data['mdq_download_json']),\
                download_data['mdq_id'])
            logging.info('after update')
        return # no need to continue with checks
    # uuid found on local db
    if metadata_uuid is not None:
        # update with found metadata uuid from db
        thread_db.db_update_media_id(download_data['mdq_download_json']['MediaID'],\
            metadata_uuid)
        # found in database so remove from download que
        thread_db.db_download_delete(download_data['mdq_id'])
        return # no need to continue with checks


def metadata_fetch(thread_db, provider_name, download_data):
    """
    Fetch main metadata for specified provider
    """
    if provider_name == 'themoviedb':
        if download_data['mdq_download_json']['ProviderMetaID'][0:2] == 'tt': # imdb id check
            tmdb_id = metadata_movie.movie_fetch_tmdb_imdb(\
                download_data['mdq_download_json']['ProviderMetaID'])
            if tmdb_id is not None:
                download_data['mdq_download_json'].update({'ProviderMetaID': str(tmdb_id)})
                thread_db.db_download_update(json.dumps(download_data['mdq_download_json']),\
                    download_data['mdq_id'])
            else:
                # TODO this is kinda bad if you have a valid id
                thread_db.db_download_update_provider('ZZ', download_data['mdq_id'])
        else:
            metadata_movie.movie_fetch_save_tmdb(thread_db,\
                download_data['mdq_download_json']['ProviderMetaID'],\
                download_data['mdq_download_json']['MetaNewID'])
            thread_db.db_download_delete(download_data['mdq_id'])
#            download_data['mdq_download_json'].update({'Status': 'FetchCastCrew'})
#            thread_db.db_download_update(json.dumps(download_data['mdq_download_json']),\
#                download_data['mdq_id'])
    elif provider_name == 'tvmaze':
        metadata_tv.tv_fetch_save_tvmaze(thread_db,\
            download_data['mdq_download_json']['ProviderMetaID'])
        thread_db.db_download_delete(download_data['mdq_id'])
    elif provider_name == 'thetvdb':
        metadata_tv.tv_fetch_save_tvdb(thread_db,\
            download_data['mdq_download_json']['ProviderMetaID'])
        thread_db.db_download_delete(download_data['mdq_id'])


def metadata_castcrew(thread_db, provider_name, download_data):
    """
    Fetch cast/crew from specified provider
    """
    if provider_name == 'themoviedb':
        metadata_movie.movie_fetch_save_tmdb_cast_crew(thread_db,\
            download_data['mdq_download_json']['ProviderMetaID'],\
            download_data['mdq_download_json']['MetaNewID'])
    # setup for FetchReview
    download_data['mdq_download_json'].update({'Status': 'FetchReview'})
    thread_db.db_download_update(json.dumps(download_data['mdq_download_json']),\
        download_data['mdq_id'])


def metadata_image(thread_db, provider_name, download_data):
    """
    Fetch image from specified provider
    """
    thread_db.db_download_delete(download_data['mdq_id'])


def metadata_review(thread_db, provider_name, download_data):
    """
    Fetch reviews from specified provider
    """
    if provider_name == 'themoviedb':
        metadata_movie.movie_fetch_save_tmdb_review(thread_db,\
            download_data['mdq_download_json']['ProviderMetaID'])
    # review is last.....so can delete download que
    thread_db.db_download_delete(download_data['mdq_id'])


def metadata_collection(thread_db, provider_name, download_data):
    """
    Fetch collection from specified provider
    """
    if provider_name == 'themoviedb':
        metadata_movie.movie_fetch_save_tmdb_collection(thread_db,\
            download_data['mdq_download_json']['ProviderMetaID'], download_data)
    # only one record for this so nuke it
    thread_db.db_download_delete(download_data['mdq_id'])
