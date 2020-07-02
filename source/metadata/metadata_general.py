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

import json

from common import common_global
from common import common_metadata_provider_chart_lyrics
from common import common_metadata_tv_theme
from guessit import guessit

from . import metadata_anime
from . import metadata_music
from . import metadata_music_video
from . import metadata_provider_imvdb
from . import metadata_provider_isbndb
from . import metadata_provider_themoviedb
from . import metadata_sports
from . import metadata_tv
from . import metadata_tv_tmdb


# from . import metadata_tv_tvdb
# from . import metadata_tv_tvmaze


def metadata_process(thread_db, provider_name, download_data, download_que_type=0):
    common_global.es_inst.com_elastic_index('info', {'metadata_process': {'provider': provider_name,
                                                                          'dl json': download_data}})
    # TODO art, posters, trailers, etc in here as well
    if download_data['mdq_download_json']['Status'] == "Search":
        metadata_search(thread_db, provider_name, download_data, download_que_type)
    elif download_data['mdq_download_json']['Status'] == "Update":
        metadata_update(thread_db, provider_name, download_data)
    elif download_data['mdq_download_json']['Status'] == "Fetch":
        metadata_fetch(thread_db, provider_name, download_data)
    elif download_data['mdq_download_json']['Status'] == "FetchCastCrew":
        metadata_castcrew(thread_db, provider_name, download_data)
    elif download_data['mdq_download_json']['Status'] == "FetchReview":
        metadata_review(thread_db, provider_name, download_data)
    elif download_data['mdq_download_json']['Status'] == "FetchImage":
        metadata_image(thread_db, provider_name, download_data)
    elif download_data['mdq_download_json']['Status'] == "FetchCollection":
        metadata_collection(thread_db, provider_name, download_data)


def metadata_update(thread_db, provider_name, download_data):
    """
    Update main metadata for specified provider
    """
    common_global.es_inst.com_elastic_index('info', {'metadata_update': provider_name,
                                                     'dldata': download_data})
    # TODO horribly broken.  Need to add the dlid, that to update, etc


def metadata_search(thread_db, provider_name, download_data, download_que_type=0):
    """
    Search for metadata via specified provider
    """
    metadata_uuid = None
    match_result = None
    set_fetch = False
    lookup_halt = False
    update_provider = None
    if provider_name == 'anidb':
        metadata_uuid = metadata_anime.metadata_anime_lookup(thread_db,
                                                             download_data,
                                                             guessit(download_data['Path'])[
                                                                 'title'])
        if metadata_uuid is None:
            if match_result is None:
                # do lookup halt as we'll start all movies in tmdb
                lookup_halt = True
            else:
                set_fetch = True
    elif provider_name == 'chart_lyrics':
        common_metadata_provider_chart_lyrics.com_meta_chart_lyrics(artist_name, song_name)
        lookup_halt = True
    elif provider_name == 'comicvine':
        lookup_halt = True
    elif provider_name == 'discogs':
        lookup_halt = True
    elif provider_name == 'giantbomb':
        lookup_halt = True
    elif provider_name == 'imdb':
        lookup_halt = True
    elif provider_name == 'imvdb':
        metadata_uuid, match_result = metadata_music_video.metadata_music_video_lookup(thread_db,
                                                                                       download_data[
                                                                                           'mdq_download_json'][
                                                                                           'Path'])
        if metadata_uuid is None:
            if match_result is None:
                update_provider = 'theaudiodb'
            else:
                set_fetch = True
    elif provider_name == 'isbndb':
        metadata_uuid, match_result = metadata_provider_isbndb.metadata_periodicals_search_isbndb(
            thread_db, download_data['mdq_download_json']['ProviderMetaID'])
        if metadata_uuid is None:
            lookup_halt = True
    elif provider_name == 'lastfm':
        lookup_halt = True
    elif provider_name == 'musicbrainz':
        metadata_uuid, match_result = metadata_music.metadata_music_lookup(thread_db,
                                                                           download_data)
        common_global.es_inst.com_elastic_index('info', {'metadata_uuid': metadata_uuid,
                                                         'result': match_result})
        if metadata_uuid is None:
            lookup_halt = True
    elif provider_name == 'omdb':
        lookup_halt = True
    elif provider_name == 'openlibrary':
        lookup_halt = True
    elif provider_name == 'pitchfork':
        lookup_halt = True
    elif provider_name == 'pornhub':
        lookup_halt = True
    elif provider_name == 'televisiontunes':
        # if download succeeds remove dl
        # TODO....handle list return for title?
        metadata_uuid = common_metadata_tv_theme.com_tvtheme_download(
            guessit(download_data['Path'])['title'])
        if metadata_uuid is not None:
            # TODO add theme.mp3 dl'd above to media table
            thread_db.db_download_delete(download_data['mdq_id'])
            return  # since it's a search/fetch/insert in one shot
        else:
            lookup_halt = True
    elif provider_name == 'theaudiodb':
        lookup_halt = True
    elif provider_name == 'thegamesdb':
        lookup_halt = True
    elif provider_name == 'themoviedb':
        if download_que_type == common_global.DLMediaType.Movie.value:
            metadata_uuid, match_result = metadata_provider_themoviedb.movie_search_tmdb(thread_db,
                                                                                         download_data[
                                                                                             'mdq_download_json'][
                                                                                             'Path'])
            common_global.es_inst.com_elastic_index('info', {'metadata_uuid': metadata_uuid,
                                                             'result': match_result})
            # if match_result is an int, that means the lookup found a match but isn't in db
            if metadata_uuid is None and type(match_result) != int:
                lookup_halt = True
            else:
                if metadata_uuid is not None:
                    set_fetch = True
        elif download_que_type == common_global.DLMediaType.TV.value:
            metadata_uuid, match_result = metadata_tv.metadata_tv_lookup(thread_db,
                                                                         download_data[
                                                                             'mdq_download_json'][
                                                                             'Path'])
            common_global.es_inst.com_elastic_index('info', {'metadata_uuid': metadata_uuid,
                                                             'result': match_result})
            # if match_result is an int, that means the lookup found a match but isn't in db
            if metadata_uuid is None and type(match_result) != int:
                lookup_halt = True
            else:
                if metadata_uuid is not None:
                    set_fetch = True
        else:
            # this will hit from type 0's (trailers, etc)
            if metadata_uuid is None:
                lookup_halt = True
            else:
                if metadata_uuid is not None:
                    set_fetch = True
    elif provider_name == 'thesportsdb':
        metadata_uuid, match_result = metadata_sports.metadata_sports_lookup(thread_db,
                                                                             download_data)
        if metadata_uuid is None:
            if match_result is None:
                update_provider = 'themoviedb'
            else:
                set_fetch = True
    # elif provider_name == 'thetvdb':
    #     metadata_uuid, match_result = metadata_tv_tvdb.tv_search_tvdb(thread_db,
    #                                                                   download_data[
    #                                                                       'mdq_download_json'][
    #                                                                       'Path'])
    #     if metadata_uuid is None:
    #         if match_result is None:
    #             lookup_halt = True
    #         else:
    #             set_fetch = True
    elif provider_name == 'tv_intros':
        lookup_halt = True
    # elif provider_name == 'tvmaze':
    #     metadata_uuid, match_result = metadata_tv_tvmaze.tv_search_tvmaze(thread_db,
    #                                                                       download_data[
    #                                                                           'mdq_download_json'][
    #                                                                           'Path'])
    #     if metadata_uuid is None:
    #         if match_result is None:
    #             update_provider = 'thetvdb'
    #         else:
    #             set_fetch = True
    elif provider_name == 'twitch':
        lookup_halt = True

    # if search is being updated to new provider
    if update_provider is not None:
        thread_db.db_download_update_provider(update_provider, download_data['mdq_id'])
        thread_db.db_commit()
        return metadata_uuid # no need to continue with checks
    # if lookup halt set to ZZ so it doesn't get picked up by metadata dl queue
    if lookup_halt:
        thread_db.db_download_update_provider('ZZ', download_data['mdq_id'])
        thread_db.db_commit()
        return metadata_uuid # no need to continue with checks
    # if set fetch, set provider id and status on dl record
    if set_fetch:
        # first verify a download queue record doesn't exist for this id
        metadata_uuid = thread_db.db_download_que_exists(download_data['mdq_id'],
                                                         download_que_type,
                                                         provider_name, str(match_result))
        common_global.es_inst.com_elastic_index('info', {'metaquelook': metadata_uuid})
        if metadata_uuid is None:
            metadata_uuid = download_data['mdq_download_json']['MetaNewID']
            common_global.es_inst.com_elastic_index('info', {'meta setfetch': metadata_uuid})
            thread_db.db_update_media_id(download_data['mdq_download_json']['MediaID'],
                                         metadata_uuid)
            download_data['mdq_download_json'].update(
                {'ProviderMetaID': str(match_result)})
            download_data['mdq_download_json'].update({'Status': 'Fetch'})
            thread_db.db_download_update(json.dumps(download_data['mdq_download_json']),
                                         download_data['mdq_id'])
            thread_db.db_commit()
    return metadata_uuid


def metadata_fetch(thread_db, provider_name, download_data):
    """
    Fetch main metadata for specified provider
    """
    common_global.es_inst.com_elastic_index('info', {'metadata_fetch': provider_name,
                                                     'dldata': download_data})
    if provider_name == 'imvdb':
        common_global.es_inst.com_elastic_index('info', {'fetch imvdb': provider_name})
        imvdb_id = metadata_provider_imvdb.movie_fetch_save_imvdb(thread_db,
                                                                  download_data[
                                                                      'mdq_download_json'][
                                                                      'ProviderMetaID'],
                                                                  download_data[
                                                                      'mdq_download_json'][
                                                                      'MetaNewID'])
    elif provider_name == 'themoviedb':
        if download_data['mdq_que_type'] == 3:  # person info
            common_global.es_inst.com_elastic_index('info', {'fetch person bio': provider_name})
            metadata_provider_themoviedb.metadata_fetch_tmdb_person(
                thread_db, provider_name, download_data)
        elif download_data['mdq_que_type'] == 0 or download_data['mdq_que_type'] == 1:  # movie
            # removing the imdb check.....as com_tmdb_metadata_by_id converts it
            metadata_provider_themoviedb.movie_fetch_save_tmdb(thread_db,
                                                               download_data['mdq_download_json'][
                                                                   'ProviderMetaID'],
                                                               download_data['mdq_download_json'][
                                                                   'MetaNewID'])
        elif download_data['mdq_que_type'] == 2:  # tv
            metadata_tv_tmdb.tv_fetch_save_tmdb(thread_db,
                                                download_data['mdq_download_json'][
                                                    'ProviderMetaID'],
                                                download_data['mdq_download_json']['MetaNewID'])
    # elif provider_name == 'thetvdb':
    #     metadata_tv_tvdb.tv_fetch_save_tvdb(thread_db,
    #                                         download_data['mdq_download_json']['ProviderMetaID'])
    # elif provider_name == 'tvmaze':
    #     metadata_tv_tvmaze.tv_fetch_save_tvmaze(thread_db,
    #                                             download_data['mdq_download_json'][
    #                                                 'ProviderMetaID'])
    thread_db.db_download_delete(download_data['mdq_id'])


def metadata_castcrew(thread_db, provider_name, download_data):
    """
    Fetch cast/crew from specified provider
    """
    if provider_name == 'themoviedb':
        metadata_provider_themoviedb.movie_fetch_save_tmdb_cast_crew(thread_db,
                                                                     download_data[
                                                                         'mdq_download_json'][
                                                                         'ProviderMetaID'],
                                                                     download_data[
                                                                         'mdq_download_json'][
                                                                         'MetaNewID'])
    # setup for FetchReview
    download_data['mdq_download_json'].update({'Status': 'FetchReview'})
    thread_db.db_download_update(json.dumps(download_data['mdq_download_json']),
                                 download_data['mdq_id'])
    thread_db.db_commit()


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
        metadata_provider_themoviedb.movie_fetch_save_tmdb_review(thread_db,
                                                                  download_data[
                                                                      'mdq_download_json'][
                                                                      'ProviderMetaID'])
    # review is last.....so can delete download que
    thread_db.db_download_delete(download_data['mdq_id'])


def metadata_collection(thread_db, provider_name, download_data):
    """
    Fetch collection from specified provider
    """
    if provider_name == 'themoviedb':
        metadata_provider_themoviedb.movie_fetch_save_tmdb_collection(thread_db,
                                                                      download_data[
                                                                          'mdq_download_json'][
                                                                          'ProviderMetaID'],
                                                                      download_data)
    # only one record for this so nuke it
    thread_db.db_download_delete(download_data['mdq_id'])
