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
import os
import uuid

from common import common_global


# imvdb lookup
def metadata_music_video_lookup(db_connection, file_name, download_que_id):
    """
    Lookup by name on music video database
    """
    # check for same variables
    if not hasattr(metadata_music_video_lookup, "metadata_last_id"):
        metadata_music_video_lookup.metadata_last_id = None  # it doesn't exist yet, so initialize it
        metadata_music_video_lookup.metadata_last_band = None
        metadata_music_video_lookup.metadata_last_song = None
    common_global.es_inst.com_elastic_index('info', {'mv file': file_name})
    # determine names
    if file_name.find('-') != -1:
        band_name, song_name = os.path.splitext(
            os.path.basename(file_name.lower()))[0].split('-', 1)
        try:
            song_name = song_name.split('(', 1)[0].strip()
        except:
            pass
        # set name for lookups
        band_name = band_name.strip().replace(' ', '-')
        song_name = song_name.strip().replace(' ', '-')
        common_global.es_inst.com_elastic_index('info', {'mv title': band_name, 'song': song_name})
        # if same as last, return last id and save lookup
        if band_name == metadata_music_video_lookup.metadata_last_band \
                and song_name == metadata_music_video_lookup.metadata_last_song:
            return metadata_music_video_lookup.metadata_last_id
        metadata_uuid = db_connection.db_meta_music_video_lookup(
            band_name, song_name)
        common_global.es_inst.com_elastic_index('info', {"uuid": metadata_uuid})
        if metadata_uuid == []:
            metadata_uuid = None
        if metadata_uuid is None:
            if IMVDB_CONNECTION is not None:
                imvdb_json = IMVDB_CONNECTION.com_imvdb_search_video(band_name, song_name)
                common_global.es_inst.com_elastic_index('info', {"imvdb return": imvdb_json})
                if imvdb_json is not None:
                    # parse the results and insert/update
                    for video_data in imvdb_json['results']:
                        # the results are bit crazy....hence the breakup and insert
                        common_global.es_inst.com_elastic_index('info', {"vid data": video_data})
                        if db_connection.db_meta_music_video_count(str(video_data['id'])) == 0:
                            # need to submit a fetch record for limiter and rest of video data
                            if db_connection.db_download_que_exists(None,
                                                                    common_global.DLMediaType.Music_Video.value,
                                                                    'imvdb',
                                                                    str(video_data['id'])) is None:
                                db_connection.db_download_insert('imvdb',
                                                                 common_global.DLMediaType.Music_Video.value,
                                                                 json.dumps({"Status": "Fetch",
                                                                             "ProviderMetaID": str(
                                                                                 video_data['id']),
                                                                             "MetaNewID": str(
                                                                                 uuid.uuid4())}))
                            # db_connection.db_meta_music_video_add(video_data['artists'][0]['slug'],
                            #                                       video_data['song_slug'], json.dumps(
                            #         {'imvdb': str(video_data['id'])}),
                            #                                       json.dumps(video_data),
                            #                                       json.dumps(
                            #                                           {'Images': {'imvdb': None}}))
                    # try after inserting new records
                    metadata_uuid = db_connection.db_meta_music_video_lookup(
                        band_name, song_name)
                    if metadata_uuid == []:
                        metadata_uuid = None
        # set last values to negate lookups for same song
        metadata_music_video_lookup.metadata_last_id = metadata_uuid
        metadata_music_video_lookup.metadata_last_band = band_name
        metadata_music_video_lookup.metadata_last_song = song_name
        return metadata_uuid
    else:
        return None
