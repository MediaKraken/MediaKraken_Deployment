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

import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("../../MediaKraken.ini")
import time
import sys
import json
import zipfile
import xmltodict

sys.path.append("../../")
sys.path.append("../../common")
from common import common_internationalization
from common import common_metadata_thetvdb
import database as database_base

# verify thetvdb key exists
if Config.get('API', 'thetvdb').strip() != 'None':
    thetvdb_api_connection = common_metadata_thetvdb.CommonMetadataTheTVDB()
else:
    thetvdb_api_connection = None

# open the database
db = database_base.MKServerDatabase()
db.db_open(Config.get('DB Connections', 'PostDBHost').strip(),
           Config.get('DB Connections', 'PostDBPort').strip(),
           Config.get('DB Connections', 'PostDBName').strip(),
           Config.get('DB Connections', 'PostDBUser').strip(),
           Config.get('DB Connections', 'PostDBPass').strip())

# pull in the zip file
tvshow_updated = 0
tvshow_inserted = 0
zip = zipfile.ZipFile('updates_all.zip', 'r')  # issues if u do RB
for zippedFile in zip.namelist():
    # grab series info
    for row_data in xmltodict.parse(zip.read(zippedFile))['Data']['Series']:
        print(row_data['id'])
        # look for previous data
        metadata_uuid = db.db_metatv_guid_by_tvdb(row_data['id'])
        if metadata_uuid is None:
            # for the individual show data
            xml_show_data, xml_actor_data, xml_banners_data \
                = thetvdb_api_connection.com_meta_thetvdb_get_zip_by_id(row_data['id'])
            # insert
            image_json = {'Images': {'thetvdb': {
                'Characters': {}, 'Episodes': {}, "Redo": True}}}
            series_id_json = json.dumps({'imdb': xml_show_data['Data']['Series']['imdb_ID'],
                                         'thetvdb': str(row_data['id']),
                                         'zap2it': xml_show_data['Data']['Series']['zap2it_id']})
            db.db_metatvdb_insert(series_id_json, xml_show_data['Data']['Series']['SeriesName'],
                                  json.dumps({'Meta': {'thetvdb': {'Meta': xml_show_data['Data'],
                                                                   'Cast': xml_actor_data,
                                                                   'Banner': xml_banners_data}}}),
                                  json.dumps(image_json))
            # insert cast info
            if xml_actor_data is not None:
                db.db_meta_person_insert_cast_crew(
                    'thetvdb', xml_actor_data['Actor'])
            tvshow_inserted += 1
            time.sleep(5)  # delays for 5 seconds
        else:
            # update instead
            # db.db_metatvdb_update(series_id_json,\
            # xml_show_data['Data']['Series']['SeriesName'], row_data['id'])
            tvshow_updated += 1
        # commit each just cuz
        db.db_commit()
    # grab banner info
    for row_data in xmltodict.parse(zip.read(zippedFile))['Data']['Banner']:
        print(row_data)
zip.close()

# send notications
if tvshow_updated > 0:
    db.db_notification_insert(common_internationalization.com_inter_number_format(tvshow_updated)
                              + " TV show(s) metadata updated.", True)
if tvshow_inserted > 0:
    db.db_notification_insert(common_internationalization.com_inter_number_format(tvshow_inserted)
                              + " TV show(s) metadata added.", True)

# commit all changes
db.db_commit()

# close DB
db.db_close()
