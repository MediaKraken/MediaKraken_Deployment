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
import time
sys.path.append("../MediaKraken_Common")
sys.path.append("../MediaKraken_Server")
import common_file
import common_logging
import MK_Common_Schedules_Direct
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')

# create the file for pid
pid_file = '../pid/' + str(os.getpid())
common_file.common_file_Save_Data(pid_file, 'Schedules Direct Update', False, False, None)


def signal_receive(signum, frame):
    print('CHILD Schedules Direct Update: Received USR1')
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


def MK_Schedules_Direct_Program_Info_Fetch(meta_program_fetch):
    logging.debug("array: %s", meta_program_fetch)
    meta_program_json = sd.MK_Common_Schedules_Direct_Program_Info(json.dumps(meta_program_fetch))
    logging.debug("result: %s", meta_program_json)
#   meta_program_json = sd.MK_Common_Schedules_Direct_Program_Desc(json.dumps([{'programID': program_json['programID']}]))
    for program_data in meta_program_json:
        db.MK_Server_Database_TV_Program_Insert(program_json['programID'], json.dumps(program_data))


# start logging
common_logging.common_logging_Start('./log/MediaKraken_Subprogram_Schedules_Direct_Updates')


# open the database
db = database_base.MK_Server_Database()
db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.MK_Server_Database_Activity_Insert('MediaKraken_Server Schedules Direct Update Start', None,\
    'System: Server Schedules Direct Start', 'ServerSchedulesDirectStart', None, None, 'System')


sd = MK_Common_Schedules_Direct.MK_Common_Schedules_Direct_API()
sd.MK_Common_Schedules_Direct_Login(Config.get('SD', 'User').strip(), Config.get('SD', 'Password').strip())
status_data = sd.MK_Common_Schedules_Direct_Status()
if status_data['systemStatus'][0]['status'] == "Online":
    pass
else:
    logging.critical("SD is unavailable")
    sys.exit(0)
# version check
# version_json = sd.MK_Common_Schedules_Direct_Client_Version()
# TODO
#if version_json != "MediaKraken_0.1.0":
#    logging.critical("Outdated Client Version! Upgrade MediaKraken_")
#    sys.exit(0)

# get headends
# headends_json = sd.MK_Common_Schedules_Direct_Headends('USA', '58701')

# add to lineup
# logging.info(sd.MK_Common_Schedules_Direct_Lineup_Add('USA-ND33420-DEFAULT'))

# remove from lineup
#logging.info(sd.MK_Common_Schedules_Direct_Lineup_Delete('USA-DISH687-DEFAULT'))


# list lineups and channels for them
#for line_name in sd.MK_Common_Schedules_Direct_Lineup_List()['lineups']:
#    # channel map
#    channel_map = sd.MK_Common_Schedules_Direct_Lineup_Channel_Map(line_name['lineup'])
#    logging.debug("Map: %s", channel_map['map'])
#    for channel_id in channel_map['map']:
#        logging.debug("mapchannel: %s", channel_id)
#        db.MK_Server_Database_TV_Station_Insert(channel_id['stationID'], channel_id['channel'])
#    logging.debug("Stations: %s", channel_map['stations'])
#    for channel_meta in channel_map['stations']:
#        logging.debug("stationschannel: %s", channel_meta)
#        db.MK_Server_Database_TV_Station_Update(channel_meta['name'], channel_meta['stationID'], json.dumps(channel_meta))


# TODO downloading a generic description of a program - good for what the show is......not an episode itself

station_fetch = []
logging.debug("list: %s", db.MK_Server_Database_TV_Stations_Read_StationID_List())
# grab all stations in DB
for station_id in db.MK_Server_Database_TV_Stations_Read_StationID_List():
    # fetch all schedules for station
    station_fetch.append(station_id['mv_tv_station_id'])


# set here so it exists at the "end" of processing
meta_program_fetch = []
# grab station info from SD
if len(station_fetch) > 5000:
    logging.critical("Too many channels!!!!  Exiting...")
elif len(station_fetch > 0:
    schedule_json = sd.MK_Common_Schedules_Direct_Schedules_By_StationID(json.dumps(station_fetch))
    # for each station in schedules results
    for station_json in schedule_json:
        # [{u'stationID': u'10093', u'metadata': {u'startDate': u'2016-06-15', u'modified': u'2016-06-14T23:07:05Z', u'md5': u'2aEwFuhZCqJSHKabBbR/Sg'}, 
        meta_program_fetch = []
       # for each program in station schedule result
        for program_json in station_json['programs']:
            # {u'ratings': [{u'body': u'USA Parental Rating', u'code': u'TV14'}], u'audioProperties': [u'DD 5.1', u'stereo'], u'duration': 9000, u'programID': u'MV000135600000', u'airDateTime': u'2016-06-15T00:30:00Z', u'md5': u'18/KxBZUiJQu5sCix7WWwQ'},
            db.MK_Server_Database_TV_Schedule_Insert(station_json['stationID'], program_json['airDateTime'], json.dumps(program_json))
            logging.debug("what: %s", program_json['programID'])
            #if program_json['programID'][0:2] != "MV":
            meta_program_fetch.append(program_json['programID'])
            if len(meta_program_fetch) >= 500:
                MK_Schedules_Direct_Program_Info_Fetch(meta_program_fetch)
                meta_program_fetch = []


# TODO check to see if meta array has unstored data
if len(meta_program_fetch) > 0:
    MK_Schedules_Direct_Program_Info_Fetch(meta_program_fetch)

# TODO, go grab images for blank logos

# log end
db.MK_Server_Database_Activity_Insert('MediaKraken_Server Schedules Direct Update Stop', None,\
    'System: Server Schedules Direct Stop', 'ServerSchedulesDirectStop', None, None, 'System')


# commit all changes to db
db.MK_Server_Database_Commit()


# close DB
db.MK_Server_Database_Close()


# remove pid
os.remove(pid_file)
