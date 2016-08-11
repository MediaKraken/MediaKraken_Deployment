'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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
sys.path.append("../common")
sys.path.append("../server")
import MK_Common_File
import MK_Common_Logging
import MK_Common_System
import os
import signal
import database as database_base
from concurrent import futures
import subprocess
from datatime import timedelta


# create the file for pid
pid_file = './pid/' + str(os.getpid())
MK_Common_File.MK_Common_File_Save_Data(pid_file, 'Sub_Sync', False, False, None)


def signal_receive(signum, frame):
    print 'CHILD Sync: Received USR1'
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.MK_Server_Database_Rollback()
    db.MK_Server_Database_Close()
    sys.stdout.flush()
    sys.exit(0)


def worker(row_data):
    logging.debug("row: %s", row_data)
    thread_db = database_base.MK_Server_Database()
    thread_db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())
    # row_data
    # 0 mm_sync_guid uuid NOT NULL, 1 mm_sync_path text, 2 mm_sync_path_to text, 3 mm_sync_options_json jsonb
    ffmpeg_params = ['ffmpeg', '-i', thread_db.MK_Server_Database_Media_Path_By_UUID(row_data['mm_sync_options_json']['Media GUID'])[0].encode('utf8')]
    if row_data['mm_sync_options_json']['Options']['Size'] != "Clone":
        ffmpeg_params.extend(('-fs', row_data['mm_sync_options_json']['Options']['Size'].encode('utf8')))
    if row_data['mm_sync_options_json']['Options']['VCodec'] != "Copy":
        ffmpeg_params.extend(('-vcodec', row_data['mm_sync_options_json']['Options']['VCodec']))
    if row_data['mm_sync_options_json']['Options']['AudioChannels'] != "Copy":
        ffmpeg_params.extend(('-ac', row_data['mm_sync_options_json']['Options']['AudioChannels'].encode('utf8')))
    if row_data['mm_sync_options_json']['Options']['ACodec'] != "Copy":
        ffmpeg_params.extend(('-acodec', row_data['mm_sync_options_json']['Options']['ACodec'].encode('utf8')))
    if row_data['mm_sync_options_json']['Options']['ASRate'] != 'Default':
        ffmpeg_params.extend(('-ar', row_data['mm_sync_options_json']['Options']['ASRate']))
    ffmpeg_params.append(row_data['mm_sync_path_to'].encode('utf8') + "." + row_data['mm_sync_options_json']['Options']['VContainer'])
    logging.debug("ffmpeg: %s", ffmpeg_params)
    ffmpeg_pid = subprocess.Popen(ffmpeg_params, shell=False, stdout=subprocess.PIPE)
    # output after it gets started
    #  Duration: 01:31:10.10, start: 0.000000, bitrate: 4647 kb/s
    # frame= 1091 fps= 78 q=-1.0 Lsize=    3199kB time=00:00:36.48 bitrate= 718.4kbits/s dup=197 drop=0 speed= 2.6x
    media_duration = None
    while True:
        line = proc.stdout.readline()
        if line != '':
            logging.debug("ffmpeg out: %", line.rstrip())
            if line.find("Duration:") != -1:
                media_duration = timedelta(line.split(': ', 1)[1].split(',', 1)[0])
            elif line[0:5] == "frame":
                time_string = timedelta(line.split('=', 5)[5].split(' ', 1)[0])
                time_percent = time_string.total_seconds() / media_duration.total_seconds()
                thread_db.MK_Server_Database_Sync_Progress_Update(row_data['mm_sync_guid'], time_percent)
                thread_db.MK_Server_Database_Commit()
        else:
            break
    ffmpeg_pid.wait()
    thread_db.MK_Server_Database_Activity_Insert(u'MediaKraken_Server Sync', None, u'System: Server Sync', u'ServerSync', None, None, u'System')
    thread_db.MK_Server_Database_Sync_Delete(row_data[0]) # guid of sync record
    #thread_db.store record in activity table
    thread_db.MK_Server_Database_Commit()
    thread_db.MK_Server_Database_Close()
    return


# start logging
MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Subprogram_Sync')


# open the database
db = database_base.MK_Server_Database()
db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.MK_Server_Database_Activity_Insert(u'MediaKraken_Server Sync Start', None, u'System: Server Sync Start', u'ServerSyncStart', None, None, u'System')


# grab some dirs to scan and thread out the scans
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# switched to this since tracebacks work this method
sync_data = db.MK_Server_Database_Sync_List()
with futures.ThreadPoolExecutor(len(sync_data)) as executor:
    futures = [executor.submit(worker, n) for n in sync_data]
    for future in futures:
        logging.debug(future.result())


# log end
db.MK_Server_Database_Activity_Insert(u'MediaKraken_Server Sync Stop', None, u'System: Server Sync Stop', u'ServerSyncStop', None, None, u'System')

# commit all changes
db.MK_Server_Database_Commit()

# close the database
db.MK_Server_Database_Close()

# remove pid
os.remove(pid_file)
