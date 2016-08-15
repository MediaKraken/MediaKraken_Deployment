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
import os
import json
import sys
sys.path.append("../common")
from common import common_metadata_imvdb
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")


# verify imvdb key exists
if Config.get('API', 'imvdb').strip() != 'None':
    imvdb_api_connection = common_metadata_imvdb.com_imvdb_API(Config.get('API', 'imvdb').strip())
else:
    imvdb_api_connection = None


# imvdb look
def imvdb_lookup(db_connection, file_name):
    """
    Lookup by name on music video database
    """
    # check for same show variables
    if not hasattr(imvdb_lookup, "metadata_last_id"):
       imvdb_lookup.metadata_last_id = None  # it doesn't exist yet, so initialize it
       imvdb_lookup.metadata_last_band = None
       imvdb_lookup.metadata_last_song = None
    # determine names
    band_name, song_name = os.path.splitext(os.path.basename(file_name.lower()))[0].split('-', 1)
    try:
        song_name = song_name.split('(', 1)[0].strip()
    except:
        pass
    # set name for lookups
    band_name = band_name.replace(' ', '-')
    song_name = song_name.replace(' ', '-')
    logging.debug('mv title: %s, %s', band_name, song_name)
    # if same as last, return last id and save lookup
    if band_name == imvdb_lookup.metadata_last_band\
            and song_name == imvdb_lookup.metadata_last_song:
        return imvdb_lookup.metadata_last_id
    metadata_uuid = db_connection.srv_db_meta_music_video_lookup(band_name, song_name)
    logging.debug("uuid: %s", metadata_uuid)
    if metadata_uuid == []:
        metadata_uuid = None
    if metadata_uuid is None:
        if imvdb_api_connection is not None:
            imvdb_json = imvdb_api_connection.com_imvdb_Search_Video(band_name, song_name)
            logging.debug("imvdb return: %s", imvdb_json)
            # parse the results and insert/udpate
            for video_data in imvdb_json['results']:
                logging.debug("vid data: %s", video_data)
                if db_connection.srv_db_meta_music_video_count(str(video_data['id'])) == 0:
                    db_connection.srv_db_meta_music_video_add(video_data['artists'][0]['slug'],\
                        video_data['song_slug'], json.dumps({'imvdb': str(video_data['id'])}),\
                        json.dumps(video_data), json.dumps({'Images': {'imvdb': None}}))
            # try after inserting new records
            metadata_uuid = db_connection.srv_db_meta_music_video_lookup(band_name, song_name)
            if metadata_uuid == []:
                metadata_uuid = None
    # set last values to negate lookups for same song
    imvdb_lookup.metadata_last_id = metadata_uuid
    imvdb_lookup.metadata_last_band = band_name
    imvdb_lookup.metadata_last_song = song_name
    return metadata_uuid


def metadata_music_video_lookup(db_connection, file_name, download_que_id):
    """
    Music Video lookup
    """
    metadata_uuid = imvdb_lookup(db_connection, file_name)
    return metadata_uuid
