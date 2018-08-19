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
import os

from common import common_config_ini
from common import common_global
from common import common_metadata_imvdb

option_config_json, db_connection = common_config_ini.com_config_read()

# verify imvdb key exists
if option_config_json['API']['imvdb'] is not None:
    IMVDB_CONNECTION \
        = common_metadata_imvdb.CommonMetadataIMVdb(option_config_json['API']['imvdb'])
else:
    IMVDB_CONNECTION = None


# imvdb look
def imvdb_lookup(db_connection, file_name):
    """
    Lookup by name on music video database
    """
    # check for same variables
    if not hasattr(imvdb_lookup, "metadata_last_id"):
        imvdb_lookup.metadata_last_id = None  # it doesn't exist yet, so initialize it
        imvdb_lookup.metadata_last_band = None
        imvdb_lookup.metadata_last_song = None
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
        if band_name == imvdb_lookup.metadata_last_band \
                and song_name == imvdb_lookup.metadata_last_song:
            return imvdb_lookup.metadata_last_id
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
                    # parse the results and insert/udpate
                    for video_data in imvdb_json['results']:
                        # the results are bit crazy....hence the breakup and insert
                        common_global.es_inst.com_elastic_index('info', {"vid data": video_data})
                        if db_connection.db_meta_music_video_count(str(video_data['id'])) == 0:
                            db_connection.db_meta_music_video_add(video_data['artists'][0]['slug'],
                                                                  video_data['song_slug'], json.dumps(
                                    {'imvdb': str(video_data['id'])}),
                                                                  json.dumps(video_data),
                                                                  json.dumps(
                                                                      {'Images': {'imvdb': None}}))
                    # try after inserting new records
                    metadata_uuid = db_connection.db_meta_music_video_lookup(
                        band_name, song_name)
                    if metadata_uuid == []:
                        metadata_uuid = None
        # set last values to negate lookups for same song
        imvdb_lookup.metadata_last_id = metadata_uuid
        imvdb_lookup.metadata_last_band = band_name
        imvdb_lookup.metadata_last_song = song_name
        return metadata_uuid
    else:
        return None


def metadata_music_video_lookup(db_connection, file_name):
    """
    Music Video lookup
    """
    metadata_uuid = imvdb_lookup(db_connection, file_name)
    return metadata_uuid
