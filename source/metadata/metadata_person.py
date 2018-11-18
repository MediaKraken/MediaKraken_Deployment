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

import time

from common import common_config_ini
from common import common_metadata_tmdb

option_config_json, db_connection = common_config_ini.com_config_read()

# verify themoviedb key exists
if option_config_json['API']['themoviedb'] is not None:
    # setup the thmdb class
    TMDB_CONNECTION = common_metadata_tmdb.CommonMetadataTMDB(
        option_config_json)
else:
    TMDB_CONNECTION = None


def metadata_fetch_tmdb_person(thread_db, provider_name, download_data):
    """
    fetch person bio
    """
    if TMDB_CONNECTION is not None:
        # common_global.es_inst.com_elastic_index('info', {"meta person tmdb save fetch":
        #                                                      download_data})
        # fetch and save json data via tmdb id
        result_json = TMDB_CONNECTION.com_tmdb_metadata_bio_by_id(
            download_data['mdq_download_json']['ProviderMetaID'])
        # common_global.es_inst.com_elastic_index('info', {"meta person code":
        #                                                      result_json.status_code})
        # common_global.es_inst.com_elastic_index('info', {"meta person save fetch result":
        #                                                      result_json.json()})
        if result_json.status_code == 200:
            thread_db.db_meta_person_update(provider_name,
                                            download_data['mdq_download_json']['ProviderMetaID'],
                                            result_json.json(),
                                            TMDB_CONNECTION.com_tmdb_meta_bio_image_build(thread_db,
                                                                                          result_json.json()))
            # commit happens in download delete
            thread_db.db_download_delete(download_data['mdq_id'])
        elif result_json.status_code == 502:
            time.sleep(60)
            metadata_fetch_tmdb_person(thread_db, provider_name, download_data)
