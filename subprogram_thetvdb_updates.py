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
import logging # pylint: disable=W0611
import sys
import os
import signal
import json
import xmltodict
import zipfile
import zlib
import time
from common import common_config_ini
from common import common_file
from common import common_logging
from common import common_metadata_thetvdb
import locale
locale.setlocale(locale.LC_ALL, '')


# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'TheTVDB Update', False, False, None)

def signal_receive(signum, frame): # pylint: disable=W0613
    """
    Handle signal interupt
    """
    print('CHILD TheTVDB Update: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db_connection.db_rollback()
    db_connection.db_close()
    sys.stdout.flush()
    sys.exit(0)

if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c # pylint: disable=E1101
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_thetvdb_Updates')


# open the database
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server thetvdb Update Start', None,\
    'System: Server thetvdb Start', 'ServerthetvdbStart', None, None, 'System')


# grab the data
tvshow_updated = 0
tvshow_inserted = 0
thetvdb_API_Connection = common_metadata_thetvdb.CommonMetadataTheTVDB(option_config_json)
option_json, status_json = db_connection.db_opt_status_read()
#for update_item in xmltodict.parse(thetvdb_API_Connection.com_meta_TheTVDB_Updates_by_Epoc(status_json['thetvdb_Updated_Epoc'])):
update_item = thetvdb_API_Connection.com_meta_thetvdb_updates()
# grab series info
for row_data in update_item['Data']['Series']:
    logging.debug(row_data['id'])
    # look for previous data
    metadata_uuid = db_connection.db_metatv_guid_by_tvdb(row_data['id'])
    if metadata_uuid is None:
        # for the individual show data
        xml_show_data, xml_actor_data, xml_banners_data\
            = thetvdb_API_Connection.com_meta_thetvdb_get_zip_by_id(row_data['id'])
        # insert
        image_json = {'Images': {'thetvdb': {'Characters': {}, 'Episodes': {}, "Redo": True}}}
        series_id_json = json.dumps({'imdb':xml_show_data['Data']['Series']['imdb_ID'],\
            'thetvdb':str(row_data['id']), 'zap2it':xml_show_data['Data']['Series']['zap2it_id']})
        db_connection.db_metatvdb_insert(series_id_json,\
            xml_show_data['Data']['Series']['SeriesName'], json.dumps({'Meta':\
                {'thetvdb': {'Meta': xml_show_data['Data'], 'Cast': xml_actor_data,\
                'Banner': xml_banners_data}}}), json.dumps(image_json))
        # insert cast info
        if xml_actor_data is not None:
            db_connection.db_meta_person_insert_cast_crew('thetvdb', xml_actor_data['Actor'])
        db_connection.db_commit()
        tvshow_inserted += 1
        time.sleep(5) # delays for 5 seconds
    else:
        # update instead
        #db_connection.db_metatvdb_update(series_id_json,\
        # xml_show_data['Data']['Series']['SeriesName'], row_data['id'])
        tvshow_updated += 1
    # commit each just cuz
    db_connection.db_commit()
# grab banner info
for row_data in xmltodict.parse(zip.read(zippedFile))['Data']['Banner']:
    logging.debug(row_data)


# set the epoc date
# TODO update the epoc in status from the udpate xml
#db_connection.db_Option_Status_Update(row_data[0], status_json)

# log end
db_connection.db_activity_insert('MediaKraken_Server thetvdb Update Stop', None,\
    'System: Server thetvdb Stop', 'ServerthetvdbStop', None, None, 'System')

# send notications
if tvshow_updated > 0:
    db_connection.db_notification_insert(locale.format('%d', tvshow_updated, True)\
        + " TV show(s) metadata updated.", True)
if tvshow_inserted > 0:
    db_connection.db_notification_insert(locale.format('%d', tvshow_inserted, True)\
        + " TV show(s) metadata added.", True)


# commit all changes
db_connection.db_commit()


# close DB
db_connection.db_close()


# remove pid
os.remove(pid_file)
