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

import json

from common import common_config_ini
from common import common_global
from common import common_metadata_musicbrainz

option_config_json, db_connection = common_config_ini.com_config_read()

if option_config_json['API']['musicbrainz'] is not None:
    # setup the mediabrainz class
    MBRAINZ_CONNECTION = common_metadata_musicbrainz.CommonMetadataMusicbrainz(option_config_json)
else:
    MBRAINZ_CONNECTION = None


def music_search_musicbrainz(db_connection, download_que_json):
    try:
        common_global.es_inst.com_elastic_index('info', {"meta music search brainz": download_que_json})
    except:
        pass
    metadata_uuid = None
    if MBRAINZ_CONNECTION is not None:
        # look at musicbrainz server
        music_data = MBRAINZ_CONNECTION.com_mediabrainz_get_recordings(
            ffmpeg_data_json['format']['tags']['ARTIST'],
            ffmpeg_data_json['format']['tags']['ALBUM'],
            ffmpeg_data_json['format']['tags']['TITLE'], return_limit=1)
        if music_data is not None:
            if metadata_uuid is None:
                metadata_uuid = db_connection.db_meta_song_add(
                    ffmpeg_data_json['format']['tags']['TITLE'],
                    music_data['fakealbun_id'], json.dumps(music_data))
    return metadata_uuid, music_data

def metadata_music_lookup(db_connection, download_que_json, download_que_id):
    """
    Music lookup
    """
    # don't bother checking title/year as the main_server_metadata_api_worker does it already
    if not hasattr(metadata_music_lookup, "metadata_last_id"):
        # it doesn't exist yet, so initialize it
        metadata_music_lookup.metadata_last_id = None
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
    common_global.es_inst.com_elastic_index('info', {"meta music lookup": download_que_json})
    metadata_uuid = None
    # get ffmpeg data from database
    ffmpeg_data_json = db_connection.db_ffprobe_data(download_que_json['MediaID'])
    common_global.es_inst.com_elastic_index('info', {"meta music ffmpeg": ffmpeg_data_json})
    # see if record is stored locally as long as there is valid tagging
    if 'format' in ffmpeg_data_json \
            and 'tags' in ffmpeg_data_json['format'] \
            and 'ARTIST' in ffmpeg_data_json['format']['tags'] \
            and 'ALBUM' in ffmpeg_data_json['format']['tags'] \
            and 'TITLE' in ffmpeg_data_json['format']['tags']:
        db_result = db_connection.db_music_lookup(ffmpeg_data_json['format']['tags']['ARTIST'],
                                                  ffmpeg_data_json['format']['tags']['ALBUM'],
                                                  ffmpeg_data_json['format']['tags']['TITLE'])
        if db_result is None:
            pass
        else:
            metadata_uuid = db_result['mm_metadata_music_guid']
    if metadata_uuid is not None:
        db_connection.db_download_delete(download_que_id)
        # fall through here to set last id's
    else:
        metadata_uuid = download_que_json['MetaNewID']
        # no matches on local database
        # search musicbrainz since not matched above via DB
        download_que_json.update({'Status': 'Search'})
        # save the updated status
        db_connection.db_download_update(json.dumps(download_que_json),
                                         download_que_id)
        # set provider last so it's not picked up by the wrong thread
        db_connection.db_download_update_provider('musicbrainz', download_que_id)
    common_global.es_inst.com_elastic_index('info',
                                            {"metadata_music_lookup return uuid": metadata_uuid})
    metadata_music_lookup.metadata_last_id = metadata_uuid
    return metadata_uuid
