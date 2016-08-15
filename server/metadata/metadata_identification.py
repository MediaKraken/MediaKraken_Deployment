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
import logging
import uuid
import os
import sys
sys.path.append("../common")
from common import common_hash
sys.path.append("./metadata")
import metadata_anime
import metadata_game
import metadata_movie
import metadata_music_video
import metadata_periodicals
import metadata_person
import metadata_sports
import metadata_tv


def metadata_identification(db_connection, class_text, media_file_path, download_que_json,\
        download_que_id):
    """
    Determine which provider to start lookup via class text
    """
    logging.debug("Ident: %s %s %s %s", class_text, media_file_path, download_que_json,\
        download_que_id)
    metadata_uuid = None
    # find data by class type
    if class_text == "Adult":
        pass
    elif class_text == "Anime":
        metadata_uuid = metadata_anime.metadata_anime_lookup(db_connection, media_file_path,
            download_que_json, download_que_id)
    elif class_text == "Book":
        metadata_uuid = metadata_periodicals.metadata_periodicals_lookup(db_connection,\
            media_file_path, download_que_json, download_que_id)
    elif class_text == "Game CHD":
        metadata_uuid = srv_db_meta_game_by_name_and_system(os.path.basename(\
            os.path.splitext(media_file_path)[0]), lookup_system_id)
        if metadata_uuid is None:
            sha1_value = common_hash.com_hash_sha1_c(media_file_path)
            metadata_uuid = db_connection.srv_db_meta_game_by_sha1(sha1_value)
    elif class_text == "Game ISO":
        metadata_uuid = srv_db_meta_game_by_name_and_system(os.path.basename(\
            os.path.splitext(media_file_path)[0]), lookup_system_id)
        if metadata_uuid is None:
            sha1_value = common_hash.com_hash_sha1_c(media_file_path)
            metadata_uuid = db_connection.srv_db_meta_game_by_sha1(sha1_value)
    elif class_text == "Game ROM":
        metadata_uuid = srv_db_meta_game_by_name_and_system(os.path.basename(\
            os.path.splitext(media_file_path)[0]), lookup_system_id)
        if metadata_uuid is None:
            sha1_hash = common_hash.com_hash_sha1_by_filename(media_file_path)
            if sha1_hash is not None:
                # TODO lookup the sha1
                pass
    elif class_text == "Home Movie":
        metadata_uuid = str(uuid.uuid4())
    elif class_text == "Magazine":
        metadata_uuid = metadata_periodicals.metadata_periodicals_lookup(db_connection,\
            media_file_path, download_que_json, download_que_id)
    elif class_text == "Movie":
        metadata_uuid = metadata_movie.metadata_movie_lookup(db_connection, media_file_path,\
            download_que_json, download_que_id)
    elif class_text == "Movie Theme":
        guid = db_connection.srv_db_read_media_Path_Like(os.path.dirname(\
            os.path.abspath(media_file_path.replace('/theme/', ''))))
        if guid is not None:
            metadata_uuid = guid
        else:
            guid = db_connection.srv_db_read_media_Path_Like(os.path.dirname(\
                os.path.abspath(media_file_path.replace('/backdrops/', ''))))
            if guid is not None:
                metadata_uuid = guid
            else:
                pass  # TODO lookup properly
    elif class_text == "Movie Trailer":
        guid = db_connection.srv_db_read_media_Path_Like(os.path.dirname(\
            os.path.abspath(media_file_path.replace('/trailers/', ''))))
        if guid is not None:
            metadata_uuid = guid
        else:
            pass  # TODO lookup properly
    elif class_text == "Music":
        metadata_uuid = metadata_music.metadata_music_lookup(db_connection, media_file_path,\
            download_que_json, download_que_id)
    elif class_text == "Music Lyric":
        # search musicbrainz as the lyrics should already be in the file/record
        pass
    elif class_text == "Music Video":
        metadata_uuid = metadata_music_video.metadata_music_video_lookup(db_connection,\
            media_file_path, download_que_json, download_que_id)
    elif class_text == "Picture":
        metadata_uuid = str(uuid.uuid4())
    elif class_text == "Sports":
        metadata_uuid = metadata_sports.metadata_sports_lookup(db_connection, media_file_path,\
            download_que_json, download_que_id)
    elif class_text == "Subtitle":
        # TODO perhaps check file name for blah.sub = blah.mkv   then the metadata id for that
        pass
    elif class_text == "TV Show":
        metadata_uuid = metadata_tv.metadata_tv_lookup(db_connection, media_file_path,\
            download_que_json, download_que_id)
    elif class_text == "TV Theme":
        guid = db_connection.srv_db_read_media_Path_Like(os.path.dirname(\
            os.path.abspath(media_file_path.replace('/theme/', ''))))
        if guid is not None:
            metadata_uuid = guid
        else:
            pass  # TODO lookup properly
    elif class_text == "TV Trailer":
        guid = db_connection.srv_db_read_media_Path_Like(os.path.dirname(\
            os.path.abspath(media_file_path.replace('/trailers/', ''))))
        if guid is not None:
            metadata_uuid = guid
        else:
            pass  # TODO lookup properly
    elif class_text == "Video Game":
        pass
    elif class_text == "Video Game Intro":
        pass
    elif class_text == "Video Game Speedrun":
        pass
    elif class_text == "Video Game Superplay":
        pass
    logging.debug("Meta id ident return: %s", metadata_uuid)
    return metadata_uuid
