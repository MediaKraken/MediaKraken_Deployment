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
import time

from common import common_global


async def movie_fetch_save_imvdb(db_connection, imvdb_id, metadata_uuid):
    """
    # fetch from imvdb
    """
    common_global.es_inst.com_elastic_index('info', {"meta imvdb save fetch": imvdb_id})
    # fetch and save json data via tmdb id
    result_json = common_global.api_instance.com_imvdb_video_info(imvdb_id)
    common_global.es_inst.com_elastic_index('info', {"meta imvdb code": result_json.status_code})
    if result_json.status_code == 200:
        common_global.es_inst.com_elastic_index('info', {"meta imvdb save fetch result":
                                                             result_json.json()})
        # set and insert the record
        db_connection.db_meta_music_video_add(metadata_uuid, json.dumps({'imvdb': str(result_json[
                                                                                          'id'])}),
                                              result_json['artists'][0]['slug'],
                                              result_json['song_slug'],
                                              json.dumps(result_json),
                                              None)
    elif result_json.status_code == 502:
        time.sleep(300)
        # redo fetch due to 502
        await movie_fetch_save_imvdb(db_connection, imvdb_id, metadata_uuid)
    elif result_json.status_code == 404:
        # TODO handle 404's better
        metadata_uuid = None
    else:  # is this is None....
        metadata_uuid = None
    common_global.es_inst.com_elastic_index('info', {'meta imvdb save fetch uuid':
                                                         metadata_uuid})
    return metadata_uuid
