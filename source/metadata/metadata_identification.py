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
import os
import uuid

from common import common_global
from common import common_hash
from common import common_logging_elasticsearch_httpx

from . import metadata_adult
from . import metadata_anime
from . import metadata_game
from . import metadata_movie
from . import metadata_music
from . import metadata_music_video
from . import metadata_periodicals
from . import metadata_sports
from . import metadata_tv


async def metadata_identification(db_connection, dl_row, guessit_file_name):
    """
    Determine which provider to start lookup via class text
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    metadata_uuid = None
    # find data by class type
    if dl_row['mdq_que_type'] == common_global.DLMediaType.Movie.value \
            or dl_row['mdq_que_type'] == common_global.DLMediaType.Movie_Extras.value \
            or dl_row['mdq_que_type'] == common_global.DLMediaType.Movie_Subtitle.value \
            or dl_row['mdq_que_type'] == common_global.DLMediaType.Movie_Theme.value \
            or dl_row['mdq_que_type'] == common_global.DLMediaType.Movie_Trailer.value:
        metadata_uuid = await metadata_movie.metadata_movie_lookup(db_connection,
                                                                   dl_row,
                                                                   guessit_file_name)
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Movie_Home.value \
            or dl_row['mdq_que_type'] == common_global.DLMediaType.Picture.value:
        metadata_uuid = uuid.uuid4()
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Adult.value:
        metadata_uuid = await metadata_adult.metadata_adult_lookup(db_connection,
                                                                   dl_row,
                                                                   guessit_file_name)
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Anime.value:
        metadata_uuid = await metadata_anime.metadata_anime_lookup(db_connection,
                                                                   dl_row,
                                                                   guessit_file_name)
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Publication_Book.value:
        metadata_uuid = await metadata_periodicals.metadata_periodicals_lookup(db_connection,
                                                                               dl_row)
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Game_CHD.value:
        metadata_uuid = await db_connection.db_meta_game_by_name_and_system(os.path.basename(
            os.path.splitext(dl_row['mdq_download_json']['Path'])[0]), lookup_system_id)
        if metadata_uuid is None:
            sha1_value = common_hash.com_hash_sha1_c(dl_row['mdq_download_json']['Path'])
            metadata_uuid = await db_connection.db_meta_game_by_sha1(sha1_value)
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Game_ISO.value:
        metadata_uuid = await db_connection.db_meta_game_by_name_and_system(os.path.basename(
            os.path.splitext(dl_row['mdq_download_json']['Path'])[0]), lookup_system_id)
        if metadata_uuid is None:
            sha1_value = common_hash.com_hash_sha1_c(dl_row['mdq_download_json']['Path'])
            metadata_uuid = await db_connection.db_meta_game_by_sha1(sha1_value)
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Game_ROM.value:
        metadata_uuid = await db_connection.db_meta_game_by_name_and_system(os.path.basename(
            os.path.splitext(dl_row['mdq_download_json']['Path'])[0]), lookup_system_id)
        if metadata_uuid is None:
            sha1_hash = common_hash.com_hash_sha1_by_filename(
                dl_row['mdq_download_json']['Path'])
            if sha1_hash is not None:
                metadata_uuid = await db_connection.db_meta_game_by_sha1(sha1_hash)
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Publication_Magazine.value:
        metadata_uuid = await metadata_periodicals.metadata_periodicals_lookup(db_connection,
                                                                               dl_row)
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Music.value:
        metadata_uuid = await metadata_music.metadata_music_lookup(db_connection,
                                                                   dl_row)
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Music_Lyrics.value:
        # search musicbrainz as the lyrics should already be in the file/record
        pass
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Music_Video.value:
        metadata_uuid = await metadata_music_video.metadata_music_video_lookup(db_connection,
                                                                               dl_row)
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Sports.value:
        metadata_uuid = await metadata_sports.metadata_sports_lookup(db_connection,
                                                                     dl_row)
    # elif class_text == "TV Extras":
    #     # include end slash so media doesn't get chopped up
    #     metadata_uuid = await db_connection.db_read_media_path_like(os.path.abspath(
    #         download_que_json['Path'].replace('/extras/', '/').rsplit('/', 1)[0]))
    #     if metadata_uuid is not None:
    #         db_connection.db_download_delete(download_que_id)
    #     else:
    #         metadata_uuid = await metadata_tv.metadata_tv_lookup(db_connection,
    #                                                        dl_row,
    #                                                        guessit_file_name)
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.TV.value:
        metadata_uuid = await metadata_tv.metadata_tv_lookup(db_connection,
                                                             dl_row,
                                                             guessit_file_name)
    # elif dl_row['mdq_que_type'] == common_global.DLMediaType.TV_Theme.value:
    #     await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text= {'stuff': 'tv theme ident'})
    #     # include end slash so theme.mp3 doesn't get chopped up
    #     await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text= {'stuff': 'tv theme ident 2'})
    #     metadata_uuid = db_connection.db_read_media_path_like(os.path.abspath(
    #         download_que_json['Path'].replace(
    #             '/theme/', '/').replace('/backdrops/', '/')
    #             .rsplit('/', 1)[0]))
    #     await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text= {'stuff': 'tv theme ident 3'})
    #     if metadata_uuid is not None:
    #         await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text= {'stuff': 'tv theme ident 4'})
    #         db_connection.db_download_delete(download_que_id)
    #     else:
    #         await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text= {'stuff': 'tv theme ident 5'})
    #         metadata_uuid = metadata_tv.metadata_tv_lookup(db_connection,
    #                                                        download_que_json,
    #                                                        download_que_id,
    #                                                        guessit_file_name)
    #         await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text= {'stuff': 'tv theme ident 6'})
    #         if metadata_uuid is None:
    #             await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text= {'stuff': 'tv theme ident 7'})
    #             # TODO so, the show hasn't been fetched yet.....so, no path match
    #             db_connection.db_download_update_provider(
    #                 'ZZ', download_que_id)
    # elif dl_row['mdq_que_type'] == common_global.DLMediaType.TV_Trailer.value:
    #     # include end slash so theme.mp3 doesn't get chopped up
    #     metadata_uuid = db_connection.db_read_media_path_like(os.path.abspath(
    #         download_que_json['Path'].replace('/trailers/', '/').rsplit('/', 1)[0]))
    #     if metadata_uuid is not None:
    #         db_connection.db_download_delete(download_que_id)
    #     else:
    #         metadata_uuid = metadata_tv.metadata_tv_lookup(db_connection,
    #                                                        dl_row,
    #                                                        guessit_file_name)
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Game.value:
        metadata_uuid = await metadata_game.metadata_game_lookup(db_connection,
                                                                 dl_row)
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Game_Intro.value:
        pass
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Game_Speedrun.value:
        pass
    elif dl_row['mdq_que_type'] == common_global.DLMediaType.Game_Superplay.value:
        pass
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text=
                                                                     {
                                                                         "metadata_identification uuid return": metadata_uuid})
    return metadata_uuid
