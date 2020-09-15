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

from common import common_logging_elasticsearch_httpx


# example ffprobe output for music file
# {"format": {"size": "9396411", "tags": {"DATE": "1996", "disc": "1", "ALBUM": "Theli", "GENRE": "Symphonic Metal",
#  "TITLE": "Preludium", "track": "01", "ARTIST": "Therion", "TOTALDISCS": "1", "TOTALTRACKS": "10"},
#  "bit_rate": "726058", "duration": "103.533333", "filename": "/home/spoot/nfsmount/Music_CD/Therion/Theli/01 - Preludium.flac", "nb_streams": 1,
#  "start_time": "0.000000", "format_name": "flac", "nb_programs": 0, "probe_score": 50, "format_long_name": "raw FLAC"},
#  "streams": [{"index": 0, "channels": 2, "duration": "103.533333", "codec_tag": "0x0000", "start_pts": 0, "time_base": "1/44100",
#  "codec_name": "flac", "codec_type": "audio", "sample_fmt": "s16", "start_time": "0.000000",
#  "disposition": {"dub": 0, "forced": 0, "lyrics": 0, "comment": 0, "default": 0, "karaoke": 0, "original": 0, "attached_pic": 0,
#  "clean_effects": 0, "visual_impaired": 0, "hearing_impaired": 0}, "duration_ts": 4565820, "sample_rate": "44100",
#  "r_frame_rate": "0/0", "avg_frame_rate": "0/0", "channel_layout": "stereo", "bits_per_sample": 0,
#  "codec_long_name": "FLAC (Free Lossless Audio Codec)", "codec_time_base": "1/44100", "codec_tag_string": "[0][0][0][0]",
#  "bits_per_raw_sample": "16"}], "chapters": []}

async def metadata_music_lookup(db_connection, download_json):
    """
    Music lookup
    """
    # don't bother checking title/year as the main_server_metadata_api_worker does it already
    if not hasattr(metadata_music_lookup, "metadata_last_id"):
        # it doesn't exist yet, so initialize it
        metadata_music_lookup.metadata_last_id = None
    common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text={
        "meta music lookup": download_json})
    metadata_uuid = None
    # get ffmpeg data from database
    ffmpeg_data_json = db_connection.db_ffprobe_data(download_json['MediaID'])
    common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text={
        "meta music ffmpeg": ffmpeg_data_json})
    # see if record is stored locally as long as there is valid tagging
    if 'format' in ffmpeg_data_json \
            and 'tags' in ffmpeg_data_json['format'] \
            and 'ARTIST' in ffmpeg_data_json['format']['tags'] \
            and 'ALBUM' in ffmpeg_data_json['format']['tags'] \
            and 'TITLE' in ffmpeg_data_json['format']['tags']:
        db_result = db_connection.db_music_lookup(ffmpeg_data_json['format']['tags']['ARTIST'],
                                                  ffmpeg_data_json['format']['tags']['ALBUM'],
                                                  ffmpeg_data_json['format']['tags']['TITLE'])
        if db_result is not None:
            metadata_uuid = db_result['mm_metadata_music_guid']
    if metadata_uuid is None:
        metadata_uuid = download_json['MetaNewID']
        # no matches on local database
        # search musicbrainz since not matched above via DB
        download_json.update({'Status': 'Search'})
        # save the updated status
        db_connection.db_begin()
        db_connection.db_download_update(json.dumps(download_json),
                                         download_json['mdq_id'])
        # set provider last so it's not picked up by the wrong thread
        db_connection.db_download_update_provider('musicbrainz', download_json['mdq_id'])
        db_connection.db_commit()
    common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text=
    {"metadata_music_lookup return uuid": metadata_uuid})
    metadata_music_lookup.metadata_last_id = metadata_uuid
    return metadata_uuid
