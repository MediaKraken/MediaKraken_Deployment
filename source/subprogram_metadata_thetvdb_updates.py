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

import xmltodict
from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch
from common import common_metadata_thetvdb
from common import common_signal

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
    'subprogram_thetvdb_updates')

# set signal exit breaks
common_signal.com_signal_set_break()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# TODO this should go through the limiter
# grab the data
thetvdb_API_Connection = common_metadata_thetvdb.CommonMetadataTheTVDB(
    option_config_json)
option_json, status_json = db_connection.db_opt_status_read()
# for update_item in xmltodict.parse(thetvdb_API_Connection.com_meta_TheTVDB_Updates_by_Epoc\
# (status_json['thetvdb_Updated_Epoc'])):
update_item = thetvdb_API_Connection.com_meta_thetvdb_updates()
# grab series info
for row_data in update_item['Data']['Series']:
    common_global.es_inst.com_elastic_index('info', {'id': row_data['id']})
    # look for previous data
    metadata_uuid = db_connection.db_metatv_guid_by_tvdb(row_data['id'])
    if metadata_uuid is None:
        # for the individual show data
        xml_show_data, xml_actor_data, xml_banners_data \
            = thetvdb_API_Connection.com_meta_thetvdb_get_zip_by_id(row_data['id'])
        # insert
        image_json = {'Images': {'thetvdb': {
            'Characters': {}, 'Episodes': {}, "Redo": True}}}
        series_id_json = json.dumps({'imdb': xml_show_data['Data']['Series']['imdb_ID'],
                                     'thetvdb': str(row_data['id']),
                                     'zap2it': xml_show_data['Data']['Series']['zap2it_id']})
        db_connection.db_metatvdb_insert(series_id_json,
                                         xml_show_data['Data']['Series']['SeriesName'],
                                         json.dumps({'Meta':
                                                         {'thetvdb': {'Meta': xml_show_data['Data'],
                                                                      'Cast': xml_actor_data,
                                                                      'Banner': xml_banners_data}}}),
                                         json.dumps(image_json))
        # insert cast info
        if xml_actor_data is not None:
            db_connection.db_meta_person_insert_cast_crew(
                'thetvdb', xml_actor_data['Actor'])
        db_connection.db_commit()
        time.sleep(5)  # delays for 5 seconds
    else:
        # update instead
        # db_connection.db_metatvdb_update(series_id_json,\
        # xml_show_data['Data']['Series']['SeriesName'], row_data['id'])
        pass
    # commit each just cuz
    db_connection.db_commit()
# grab banner info
for row_data in xmltodict.parse(zip.read(zippedFile))['Data']['Banner']:
    common_global.es_inst.com_elastic_index('info', {'banner': row_data})

# set the epoc date
# TODO update the epoc in status from the udpate xml
# db_connection.db_Option_Status_Update(row_data[0], status_json)


# commit all changes
db_connection.db_commit()

# close DB
db_connection.db_close()
