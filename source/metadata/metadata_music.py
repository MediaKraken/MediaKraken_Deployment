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
from common import common_metadata_musicbrainz

option_config_json, db_connection = common_config_ini.com_config_read()

if option_config_json['API']['musicbrainz'] is not None:
    # setup the mediabrainz class
    mbrainz_api_connection \
        = common_metadata_musicbrainz.CommonMetadataMusicbrainz(option_config_json)
else:
    mbrainz_api_connection = None


def metadata_music_lookup(db_connection, media_file_path, download_que_id):
    """
    Search musicbrainz
    """
    # 0-mm_media_guid uuid NOT NULL,
    # 1-mm_media_class_guid uuid,
    # 2-mm_media_metadata_guid uuid,
    # 3-mm_media_path text,
    # 4-mm_media_ffprobe_json jsonb,
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
    # 5-mm_media_json jsonb,
    # see if record is stored locally
    if row_data[4] is not None:
        ffmpeg_data_json = row_data[4]
        print("what:", ffmpeg_data_json['format']['tags']['ARTIST'],
              ffmpeg_data_json['format']['tags']['ALBUM'],
              ffmpeg_data_json['format']['tags']['TITLE'])
        db_result = db_connection.db_music_lookup(ffmpeg_data_json['format']['tags']['ARTIST'],
                                                  ffmpeg_data_json['format']['tags']['ALBUM'],
                                                  ffmpeg_data_json['format']['tags']['TITLE'])
        if db_result is None:
            if mbrainz_api_connection is not None:
                # look at musicbrainz server
                brainz_id = None
                music_data = mbrainz_api_connection.com_Mediabrainz_Get_Recordings(
                    ffmpeg_data_json['format']['tags']['ARTIST'],
                    ffmpeg_data_json['format']['tags']['ALBUM'],
                    ffmpeg_data_json['format']['tags']['TITLE'], 1)
                # TODO  if not, store it
                # TODO  use the metadata id for record update
                metadata_uuid = music_data
        else:
            metadata_uuid = db_result[0]
            brainz_id = db_result[1]
        if brainz_id is not None:
            media_id_json = json.dumps({'Mbrainz': brainz_id})  # release id as that's indiv song
    elif class_text == "Music Album":
        # search musicbrainz
        # mbrainz_api_connection.com_Mediabrainz_Get_Releases()
        pass
