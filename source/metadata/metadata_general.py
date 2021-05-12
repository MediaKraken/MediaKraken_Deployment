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

import inspect

from common import common_global
from common import common_logging_elasticsearch_httpx
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


async def metadata_process(db_connection, provider_name, download_data):
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    # TODO art, posters, trailers, etc in here as well
    if download_data['mdq_status'] == "Search":
        await metadata_search(db_connection, provider_name, download_data)
    elif download_data['mdq_status'] == "Update":
        await metadata_update(db_connection, provider_name, download_data)
    elif download_data['mdq_status'] == "Fetch":
        await metadata_fetch(db_connection, provider_name, download_data)
    elif download_data['mdq_status'] == "FetchCastCrew":
        await metadata_castcrew(db_connection, provider_name, download_data)
    elif download_data['mdq_status'] == "FetchReview":
        await metadata_review(db_connection, provider_name, download_data)
    elif download_data['mdq_status'] == "FetchImage":
        await metadata_image(db_connection, provider_name, download_data)
    elif download_data['mdq_status'] == "FetchCollection":
        await metadata_collection(db_connection, provider_name, download_data)


async def metadata_update(db_connection, provider_name, download_data):
    """
    Update main metadata for specified provider
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    # TODO horribly broken.  Need to add the dlid, that to update, etc


async def metadata_search(db_connection, provider_name, download_data):
    """
    Search for metadata via specified provider
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    metadata_uuid = None
    match_result = None
    set_fetch = False
    lookup_halt = False
    update_provider = None
    if provider_name == 'anidb':
        metadata_uuid = await metadata_anime.metadata_anime_lookup(db_connection,
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
        metadata_uuid, match_result = await metadata_music_video.metadata_music_video_lookup(
            db_connection,
            download_data['mdq_path'])
        if metadata_uuid is None:
            if match_result is None:
                update_provider = 'theaudiodb'
            else:
                set_fetch = True
    elif provider_name == 'isbndb':
        metadata_uuid, match_result = await metadata_provider_isbndb.metadata_periodicals_search_isbndb(
            db_connection, download_data['mdq_provider_id'])
        if metadata_uuid is None:
            lookup_halt = True
    elif provider_name == 'lastfm':
        lookup_halt = True
    elif provider_name == 'musicbrainz':
        metadata_uuid, match_result = await metadata_music.metadata_music_lookup(db_connection,
                                                                                 download_data)
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'metadata_uuid': metadata_uuid,
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
            await db_connection.db_download_delete(download_data['mdq_id'])
            await db_connection.db_commit()
            return  # since it's a search/fetch/insert in one shot
        else:
            lookup_halt = True
    elif provider_name == 'theaudiodb':
        lookup_halt = True
    elif provider_name == 'thegamesdb':
        lookup_halt = True
    elif provider_name == 'themoviedb':
        if download_data['mdq_que_type'] == common_global.DLMediaType.Movie.value:
            metadata_uuid, match_result = await metadata_provider_themoviedb.movie_search_tmdb(
                db_connection,
                download_data['mdq_path'])
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 'metadata_uuid': metadata_uuid,
                                                                                 'result': match_result})
            # if match_result is an int, that means the lookup found a match but isn't in db
            if metadata_uuid is None and type(match_result) != int:
                lookup_halt = True
            else:
                if metadata_uuid is not None:
                    set_fetch = True
        elif download_data['mdq_que_type'] == common_global.DLMediaType.TV.value:
            metadata_uuid, match_result = await metadata_tv.metadata_tv_lookup(db_connection,
                                                                               download_data[
                                                                                   'mdq_path'])
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 'metadata_uuid': metadata_uuid,
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
        metadata_uuid, match_result = await metadata_sports.metadata_sports_lookup(db_connection,
                                                                                   download_data)
        if metadata_uuid is None:
            if match_result is None:
                update_provider = 'themoviedb'
            else:
                set_fetch = True
    elif provider_name == 'tv_intros':
        lookup_halt = True
    elif provider_name == 'twitch':
        lookup_halt = True

    # if search is being updated to new provider
    if update_provider is not None:
        await db_connection.db_download_update_provider(update_provider, download_data['mdq_id'])
        await db_connection.db_commit()
        return metadata_uuid  # no need to continue with checks
    # if lookup halt set to ZZ so it doesn't get picked up by metadata dl queue
    if lookup_halt:
        await db_connection.db_download_update_provider('ZZ', download_data['mdq_id'])
        await db_connection.db_commit()
        return metadata_uuid  # no need to continue with checks
    # if set fetch, set provider id and status on dl record
    if set_fetch:
        # first verify a download queue record doesn't exist for this id
        metadata_uuid = await db_connection.db_download_que_exists(download_data['mdq_id'],
                                                                   download_data['mdq_id'],
                                                                   provider_name, str(match_result))
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'metaquelook': metadata_uuid})
        if metadata_uuid is None:
            metadata_uuid = download_data['mdq_new_uuid']
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 'meta setfetch': metadata_uuid})
            await db_connection.db_update_media_id(download_data['mdq_provider_id'],
                                                   metadata_uuid)
            download_data['mdq_download_json'].update(
                {'ProviderMetaID': match_result})
            download_data['mdq_download_json'].update({'Status': 'Fetch'})
            await db_connection.db_download_update(download_data['mdq_download_json'],
                                                   download_data['mdq_id'])
            await db_connection.db_commit()
    return metadata_uuid


async def metadata_fetch(db_connection, provider_name, download_data):
    """
    Fetch main metadata for specified provider
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    if provider_name == 'imvdb':
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'fetch imvdb': provider_name})
        imvdb_id = await metadata_provider_imvdb.movie_fetch_save_imvdb(db_connection,
                                                                        download_data['mdq_provider_id'],
                                                                        download_data[
                                                                            'mdq_new_uuid'])
    elif provider_name == 'themoviedb':
        if download_data['mdq_que_type'] == common_global.DLMediaType.Person.value:
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 'fetch person bio': provider_name})
            await metadata_provider_themoviedb.metadata_fetch_tmdb_person(
                db_connection, provider_name, download_data)
        elif download_data['mdq_que_type'] == common_global.DLMediaType.Movie.value:
            # removing the imdb check.....as com_tmdb_metadata_by_id converts it
            await metadata_provider_themoviedb.movie_fetch_save_tmdb(db_connection,
                                                                     download_data[
                                                                         'mdq_provider_id'],
                                                                     download_data[
                                                                         'mdq_new_uuid'])
        elif download_data['mdq_que_type'] == common_global.DLMediaType.TV.value:
            await metadata_tv_tmdb.tv_fetch_save_tmdb(db_connection,
                                                      download_data['mdq_provider_id'],
                                                      download_data['mdq_new_uuid'])
    await db_connection.db_download_delete(download_data['mdq_id'])
    await db_connection.db_commit()


async def metadata_castcrew(db_connection, provider_name, download_data):
    """
    Fetch cast/crew from specified provider
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    # removed themoviedb call as it should be done during the initial fetch
    # setup for FetchReview
    download_data['mdq_download_json'].update({'Status': 'FetchReview'})
    await db_connection.db_download_update(download_data['mdq_download_json'],
                                           download_data['mdq_id'])
    await db_connection.db_commit()


async def metadata_image(db_connection, provider_name, download_data):
    """
    Fetch image from specified provider
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    await db_connection.db_download_delete(download_data['mdq_id'])
    await db_connection.db_commit()


async def metadata_review(db_connection, provider_name, download_data):
    """
    Fetch reviews from specified provider
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    if provider_name == 'themoviedb':
        await metadata_provider_themoviedb.movie_fetch_save_tmdb_review(db_connection,
                                                                        download_data[
                                                                            'mdq_provider_id'])
    # review is last.....so can delete download que
    await db_connection.db_download_delete(download_data['mdq_id'])
    await db_connection.db_commit()


async def metadata_collection(db_connection, provider_name, download_data):
    """
    Fetch collection from specified provider
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    if provider_name == 'themoviedb':
        await metadata_provider_themoviedb.movie_fetch_save_tmdb_collection(db_connection,
                                                                            download_data[
                                                                                'mdq_provider_id'],
                                                                            download_data)
    # only one record for this so nuke it
    await db_connection.db_download_delete(download_data['mdq_id'])
    await db_connection.db_commit()
