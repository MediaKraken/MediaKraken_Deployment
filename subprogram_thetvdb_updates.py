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
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import sys
import os
import signal
import json
import xmltodict
import zipfile
import zlib
import time
sys.path.append("../MediaKraken_Common")
sys.path.append("../MediaKraken_Server")
import MK_Common_File
import MK_Common_Logging
import MK_Common_Metadata_TheTVDB
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')


# create the file for pid
pid_file = '../pid/' + str(os.getpid())
MK_Common_File.MK_Common_File_Save_Data(pid_file, 'TheTVDB Update', False, False, None)

def signal_receive(signum, frame):
    print('CHILD TheTVDB Update: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.MK_Server_Database_Rollback()
    db.MK_Server_Database_Close()
    sys.stdout.flush()
    sys.exit(0)

if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# start logging
MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Subprogram_theTVDB_Updates')


# open the database
db = database_base.MK_Server_Database()
db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.MK_Server_Database_Activity_Insert('MediaKraken_Server theTVDB Update Start', None,\
    'System: Server theTVDB Start', 'ServertheTVDBStart', None, None, 'System')


# grab the data
tvshow_updated = 0
tvshow_inserted = 0
theTVDB_API_Connection = MK_Common_Metadata_TheTVDB.MK_Common_Metadata_TheTVDB_API()
option_json, status_json = db.MK_Server_Database_Option_Status_Read()
#for update_item in xmltodict.parse(theTVDB_API_Connection.MK_Common_Metadata_TheTVDB_Updates_By_Epoc(status_json['theTVDB_Updated_Epoc'])):
update_item = theTVDB_API_Connection.MK_Common_Metadata_TheTVDB_Updates()
# grab series info
for row_data in update_item['Data']['Series']:
    logging.debug(row_data['id'])
    # look for previous data
    metadata_uuid = db.MK_Server_Database_MetadataTV_GUID_By_TVDB(row_data['id'])
    if metadata_uuid is None:
        # for the individual show data
        xml_show_data, xml_actor_data, xml_banners_data = theTVDB_API_Connection.MK_Common_Metadata_TheTVDB_Get_ZIP_By_ID(row_data['id'])
        # insert
        image_json = {'Images': {'theTVDB': {'Characters': {}, 'Episodes': {}, "Redo": True}}}
        series_id_json = json.dumps({'IMDB':xml_show_data['Data']['Series']['IMDB_ID'], 'theTVDB':str(row_data['id']), 'zap2it':xml_show_data['Data']['Series']['zap2it_id']})
        db.MK_Server_Database_MetadataTVDB_Insert(series_id_json, xml_show_data['Data']['Series']['SeriesName'], json.dumps({'Meta': {'theTVDB': {'Meta': xml_show_data['Data'], 'Cast': xml_actor_data, 'Banner': xml_banners_data}}}), json.dumps(image_json))
        # insert cast info
        if xml_actor_data is not None:
            db.MK_Server_Database_Metadata_Person_Insert_Cast_Crew('theTVDB', xml_actor_data['Actor'])
        db.MK_Server_Database_Commit()
        tvshow_inserted += 1
        time.sleep(5) # delays for 5 seconds
    else:
        # update instead
        #db.MK_Server_Database_MetadataTVDB_Update(series_id_json, xml_show_data['Data']['Series']['SeriesName'], row_data['id'])
        tvshow_updated += 1
    # commit each just cuz
    db.MK_Server_Database_Commit()
# grab banner info
for row_data in xmltodict.parse(zip.read(zippedFile))['Data']['Banner']:
    logging.debug(row_data)


# set the epoc date
# TODO update the epoc in status from the udpate xml
#db.MK_Server_Database_Option_Status_Update(row_data[0], status_json)

# log end
db.MK_Server_Database_Activity_Insert('MediaKraken_Server theTVDB Update Stop', None,\
    'System: Server theTVDB Stop', 'ServertheTVDBStop', None, None, 'System')

# send notications
if tvshow_updated > 0:
    db.MK_Server_Database_Notification_Insert(locale.format('%d', tvshow_updated, True)\
        + " TV show(s) metadata updated.", True)
if tvshow_inserted > 0:
    db.MK_Server_Database_Notification_Insert(locale.format('%d', tvshow_inserted, True)\
        + " TV show(s) metadata added.", True)


# commit all changes
db.MK_Server_Database_Commit()


# close DB
db.MK_Server_Database_Close()


# remove pid
os.remove(pid_file)
