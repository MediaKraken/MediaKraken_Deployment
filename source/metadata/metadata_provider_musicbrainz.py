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
import json
import time

import musicbrainzngs
from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_version

'''
A musicbrainz release represents the unique release (i.e. issuing) of a product on a
specific date with specific release information such as the country, label, barcode,
packaging, etc. If you walk into a store and purchase an album or single, they're each
represented in musicbrainz as one release.

A recording is an entity in musicbrainz which can be linked to tracks on releases.
Each track must always be associated with a single recording, but a recording can
be linked to any number of tracks.

'''


class CommonMetadataMusicbrainz:
    """
    Class for interfacing with musicbrainz
    """

    def __init__(self, option_config_json):
        # If you plan to submit data, authenticate
        # musicbrainzngs.auth(option_config_json.get('MediaBrainz','User').strip(),
        # option_config_json.get('MediaBrainz','Password').strip())
        musicbrainzngs.set_useragent("MediaKraken_Server", common_version.APP_VERSION,
                                     "spootdev@gmail.com "
                                     "https://github.com/MediaKraken/MediaKraken_Deployment")
        if option_config_json['Docker Instances']['musicbrainz']:
            musicbrainzngs.set_hostname('mkstack_mkmusicbrainz:5000')
        else:
            # If you are connecting to a development server
            if option_config_json['Metadata']['MusicBrainz']['Host'] is not None:
                if option_config_json['Metadata']['MusicBrainz']['Host'] != 'Docker':
                    musicbrainzngs.set_hostname(
                        option_config_json['Metadata']['MusicBrainz']['Host'] + ':'
                        + option_config_json['Metadata']['MusicBrainz']['Port'])

    async def show_release_details(self, rel):
        """
        Get release details
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
        # "artist-credit-phrase" is a flat string of the credited artists
        # joined with " + " or whatever is given by the server.
        # You can also work with the "artist-credit" list manually.
        # print "{}, by {}".format(rel['title'], rel["artist-credit-phrase"])
        if 'date' in rel:
            pass
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            "musicbrainz ID": "{}".format(rel['id'])})

    async def com_mediabrainz_get_releases(self, disc_id=None, artist_name=None,
                                           artist_recording=None, return_limit=5,
                                           strict_flag=False):
        """
        # search by artist and album name
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
        if disc_id is not None:
            result = musicbrainzngs.get_releases_by_discid(disc_id,
                                                           includes=["artists", "recordings"])
        else:
            result = musicbrainzngs.search_releases(artist=artist_name, release=artist_recording,
                                                    limit=return_limit, strict=strict_flag)
        if not result['release-list']:
            common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='error',
                                                                       message_text={
                                                                           'stuff': "no release found"})
            return None
        else:
            for (idx, release) in enumerate(result['release-list']):
                common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                           message_text={
                                                                               "match #{}:".format(
                                                                                   idx + 1)})
                self.show_release_details(release)
            return release['id']

    async def com_mediabrainz_get_recordings(self, artist_name=None, release_name=None,
                                             song_name=None, return_limit=5, strict_flag=False):
        """
        # search by artist and song name
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
        result = musicbrainzngs.search_recordings(artist=artist_name, release=release_name,
                                                  recording=song_name, limit=return_limit,
                                                  strict=strict_flag)
        if not result['recording-list']:
            common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='error',
                                                                       message_text={
                                                                           'stuff': "no recording found"})
            return None
        else:
            for (idx, release) in enumerate(result['recording-list']):
                common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                           message_text={
                                                                               "match #{}:".format(
                                                                                   idx + 1)})
                self.show_release_details(release)
            return release['id']


async def music_search_musicbrainz(db_connection, ffmpeg_data_json):
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    metadata_uuid = None
    # look at musicbrainz server
    music_data = await common_global.api_instance.com_mediabrainz_get_recordings(
        ffmpeg_data_json['format']['tags']['ARTIST'],
        ffmpeg_data_json['format']['tags']['ALBUM'],
        ffmpeg_data_json['format']['tags']['TITLE'], return_limit=1)
    if music_data is not None:
        if metadata_uuid is None:
            metadata_uuid = db_connection.db_meta_song_add(
                ffmpeg_data_json['format']['tags']['TITLE'],
                music_data['fakealbun_id'], json.dumps(music_data))
    return metadata_uuid, music_data


async def music_fetch_save_musicbrainz(db_connection, tmdb_id, metadata_uuid):
    """
    # fetch from musicbrainz
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
    result_json = TMDB_CONNECTION.com_tmdb_metadata_by_id(tmdb_id)
    if result_json is not None:
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             "meta movie code": result_json.status_code,
                                                                             "header": result_json.headers})
    # 504	Your request to the backend server timed out. Try again.
    if result_json is None or result_json.status_code == 504:
        time.sleep(60)
        # redo fetch due to 504
        movie_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid)
    elif result_json.status_code == 200:
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             "meta movie save fetch result":
                                                                                 result_json.json()})
        series_id_json, result_json, image_json \
            = TMDB_CONNECTION.com_tmdb_meta_info_build(result_json.json())
        # set and insert the record
        meta_json = ({'Meta': {'themoviedb': {'Meta': result_json}}})
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             "series": series_id_json})
        # set and insert the record
        try:
            await db_connection.db_meta_insert_tmdb(metadata_uuid, series_id_json,
                                                    result_json['title'], json.dumps(meta_json),
                                                    json.dumps(image_json))
            if 'credits' in result_json:  # cast/crew doesn't exist on all media
                if 'cast' in result_json['credits']:
                    await db_connection.db_meta_person_insert_cast_crew('themoviedb',
                                                                        result_json['credits'][
                                                                            'cast'])
                if 'crew' in result_json['credits']:
                    await db_connection.db_meta_person_insert_cast_crew('themoviedb',
                                                                        result_json['credits'][
                                                                            'crew'])
        # this except is to check duplicate keys for mm_metadata_pk
        except psycopg2.IntegrityError:
            # TODO technically I could be missing cast/crew if the above doesn't finish after the insert
            pass
    # 429	Your request count (#) is over the allowed limit of (40).
    elif result_json.status_code == 429:
        time.sleep(10)
        # redo fetch due to 504
        await movie_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid)
    elif result_json.status_code == 404:
        # TODO handle 404's better
        metadata_uuid = None
    else:  # is this is None....
        metadata_uuid = None
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'meta movie save fetch uuid':
                                                                             metadata_uuid})
    return metadata_uuid
