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
import logging # pylint: disable=W0611
from common import common_cloud
from common import common_config_ini
from common import common_logging
from common import common_signal
from common import common_xfer
from concurrent import futures
import subprocess
from datetime import timedelta


def worker(row_data):
    """
    Worker ffmpeg thread for each sync job
    """
    logging.info("row: %s", row_data)
    # open the database
    option_config_json, thread_db = common_config_ini.com_config_read()
    # row_data
    # 0 mm_sync_guid uuid NOT NULL, 1 mm_sync_path text, 2 mm_sync_path_to text,
    # 3 mm_sync_options_json jsonb
    ffmpeg_params = ['./bin/ffmpeg', '-i', thread_db.db_media_path_by_uuid(\
        row_data['mm_sync_options_json']['Media GUID'])[0]]
    if row_data['mm_sync_options_json']['Options']['Size'] != "Clone":
        ffmpeg_params.extend(('-fs',\
            row_data['mm_sync_options_json']['Options']['Size']))
    if row_data['mm_sync_options_json']['Options']['VCodec'] != "Copy":
        ffmpeg_params.extend(('-vcodec', row_data['mm_sync_options_json']['Options']['VCodec']))
    if row_data['mm_sync_options_json']['Options']['AudioChannels'] != "Copy":
        ffmpeg_params.extend(('-ac',\
            row_data['mm_sync_options_json']['Options']['AudioChannels']))
    if row_data['mm_sync_options_json']['Options']['ACodec'] != "Copy":
        ffmpeg_params.extend(('-acodec',\
            row_data['mm_sync_options_json']['Options']['ACodec']))
    if row_data['mm_sync_options_json']['Options']['ASRate'] != 'Default':
        ffmpeg_params.extend(('-ar', row_data['mm_sync_options_json']['Options']['ASRate']))
    ffmpeg_params.append(row_data['mm_sync_path_to'] + "."\
        + row_data['mm_sync_options_json']['Options']['VContainer'])
    logging.info("ffmpeg: %s", ffmpeg_params)
    ffmpeg_pid = subprocess.Popen(ffmpeg_params, shell=False, stdout=subprocess.PIPE)
    # output after it gets started
    #  Duration: 01:31:10.10, start: 0.000000, bitrate: 4647 kb/s
    # frame= 1091 fps= 78 q=-1.0 Lsize=    3199kB time=00:00:36.48
    # bitrate= 718.4kbits/s dup=197 drop=0 speed= 2.6x
    media_duration = None
    while True:
        line = ffmpeg_pid.stdout.readline()
        if line != '':
            logging.info('ffmpeg out: %' % line.rstrip())
            if line.find("Duration:") != -1:
                media_duration = timedelta(line.split(': ', 1)[1].split(',', 1)[0])
            elif line[0:5] == "frame":
                time_string = timedelta(line.split('=', 5)[5].split(' ', 1)[0])
                time_percent = time_string.total_seconds() / media_duration.total_seconds()
                thread_db.db_sync_progress_update(row_data['mm_sync_guid'],\
                    time_percent)
                thread_db.db_commit()
        else:
            break
    ffmpeg_pid.wait()
    # deal with converted file
    if row_data['mm_sync_options_json']['Type'] == 'Local File System':
        # just go along merry way as ffmpeg shoulda output to mm_sync_path_to
        pass
    elif row_data['mm_sync_options_json']['Type'] == 'Remote Client':
        XFER_THREAD = common_xfer.FileSenderThread(row_data['mm_sync_options_json']['TargetIP'],\
            row_data['mm_sync_options_json']['TargetPort'],\
            row_data['mm_sync_path_to'] + "."\
            + row_data['mm_sync_options_json']['Options']['VContainer'],\
            row_data['mm_sync_path_to'])
    else: # cloud item
        CLOUD_HANDLE = common_cloud.CommonCloud()
        CLOUD_HANDLE.com_cloud_file_store(row_data['mm_sync_options_json']['Type'],\
            row_data['mm_sync_path_to'], row_data['mm_sync_path_to'] + "."\
            + row_data['mm_sync_options_json']['Options']['VContainer'].split('/', 1)[1], False)
    thread_db.db_activity_insert('MediaKraken_Server Sync', None,\
        'System: Server Sync', 'ServerSync', None, None, 'System')
    thread_db.db_sync_delete(row_data[0]) # guid of sync record
    #thread_db.store record in activity table
    thread_db.db_commit()
    thread_db.db_close()
    return


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Sync')


# open the database
option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server Sync Start', None,\
    'System: Server Sync Start', 'ServerSyncStart', None, None, 'System')


# switched to this since tracebacks work this method
sync_data = db_connection.db_sync_list()
with futures.ThreadPoolExecutor(len(sync_data)) as executor:
    futures = [executor.submit(worker, n) for n in sync_data]
    for future in futures:
        logging.info(future.result())


# log end
db_connection.db_activity_insert('MediaKraken_Server Sync Stop', None,\
    'System: Server Sync Stop', 'ServerSyncStop', None, None, 'System')


# commit all changes
db_connection.db_commit()


# close the database
db_connection.db_close()
