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

from __future__ import division
# pull in the ini file config
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import sys
sys.path.append("../MediaKraken_Common")
sys.path.append("./")  # for db import
import MK_Common_CIFS
import MK_Common_FFMPEG
import MK_Common_File
import MK_Common_Logging
import MK_Common_String
#import MK_Common_System
import _strptime # to handle threading
from datetime import datetime # to handle threading
import os
import uuid
import signal
from concurrent import futures
import database as database_base
import logging
import time
import json
import locale
locale.setlocale(locale.LC_ALL, '')
#lock = threading.Lock()


media_extension = [
    'webm',
    'mkv',
    'flv',
    'vob',
    'ogv',
    'ogg',
    'drc',
    'mng',
    'avi',
    'mov',
    'qt',
    'wmv',
    'wma',
    'yuv',
    'rm',
    'rmvb',
    'asf',
    'mp4',
    'm4p',
    'm4v',
    'mpg',
    'mp2',
    'mpeg',
    'mpe',
    'mp3',
    'flac',
    'mpv',
    'm2v',
    'm4v',
    'nsv',
    'iso',
    'chd',
    'zip',
    '7z',
    'pdf'
]


media_extension_skip_ffmpeg = [
    'pdf',
    'zip',
    '7z',
    'iso',
    'chd'
]


# create the file for pid
pid_file = './pid/' + str(os.getpid())
MK_Common_File.MK_Common_File_Save_Data(pid_file, 'Sub_File_Scan', False, False, None)


# start logging
MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Subprogram_File_Scan')


def signal_receive(signum, frame):
    print 'CHILD File Scan: Received USR1'
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.MK_Server_Database_Rollback()
    db.MK_Server_Database_Close()
    sys.stdout.flush()
    sys.exit(0)


# TODO move this into worker function......no reason for this to be seperate anymore
# perform media scan
def MK_Server_Media_Scan_Audit(thread_db, dir_path, media_class_type_uuid, known_media_file, dir_guid, class_text_dict):
    total_files = 0
    logging.info("Scan dir: %s %s", dir_path, media_class_type_uuid)
    # update the timestamp now so any other media added DURING this scan don't get skipped
    thread_db.MK_Server_Database_Audit_Directory_Timestamp_Update(dir_path)
    thread_db.MK_Server_Database_Audit_Path_Update_Status(dir_guid, json.dumps({'Status': 'File scan', 'Pct': 100}))
    thread_db.MK_Server_Database_Commit()
    # check for UNC before grabbing dir list
    if dir_path[:1] == "\\":
        file_data = []
        smb_stuff = MK_Common_CIFS.MK_Common_CIFS_Share_API()
        addr, share, path = MK_Common_String.UNC_To_Addr_Share_Path(dir_path)
        smb_stuff.MK_Common_CIFS_Connect(addr)
        for dir_data in smb_stuff.MK_Common_CIFS_Walk(share, path):
            for file_name in dir_data[2]:
                file_data.append('\\\\' + addr + '\\' + share + '\\' + dir_data[0] + '\\' + file_name)
        smb_stuff.MK_Common_CIFS_Close()
    else:
        file_data = MK_Common_File.MK_Common_File_Dir_List(dir_path, None, True, False)
    total_file_in_dir = len(file_data)
    total_scanned = 0
    for file_name in file_data:
        # TODO whined about converting both to utf8
        if file_name in known_media_file:
            pass # already scanned, skip
        else:
            fileName, fileExtension = os.path.splitext(file_name)
            if fileExtension[1:].lower() in media_extension:
                total_files += 1
                fileName, fileExtension = os.path.splitext(file_name)
                new_class_type_uuid = media_class_type_uuid
                # video game data, don't do ffmpeg
                if thread_db.MK_Server_Database_Media_Class_By_UUID(media_class_type_uuid) == 'Video Game':
                    if fileExtension.lower() == 'iso':
                        new_class_type_uuid = class_text_dict['Game ISO']
                    elif fileExtension.lower() == 'chd':
                        new_class_type_uuid = class_text_dict['Game CHD']
                    else:
                        new_class_type_uuid = class_text_dict['Game ROM']
                    # TODO lookup game info in game database data
                    media_ffprobe_json = None
                # if an extention skip
                elif fileExtension.lower() in media_extension_skip_ffmpeg:
                    media_ffprobe_json = None
                else:
                    if file_name.find('/trailers/') != -1 or file_name.find('/theme.mp3') != -1 or file_name.find('/theme.mp4') != -1 or file_name.find('\\trailers\\') != -1 or file_name.find('\\theme.mp3') != -1 or file_name.find('\\theme.mp4') != -1:
                        media_class_text = thread_db.MK_Server_Database_Media_Class_By_UUID(new_class_type_uuid)
                        if media_class_text == 'Movie':
                            if file_name.find('/trailers/') != -1 or file_name.find('\\trailers\\') != -1:
                                new_class_type_uuid = class_text_dict['Movie Trailer']
                            else:
                                new_class_type_uuid = class_text_dict['Movie Theme']
                        elif media_class_text == 'TV Show' or media_class_text == 'TV Episode' or media_class_text == 'TV Season':
                            if file_name.find('/trailers/') != -1 or file_name.find('\\trailers\\') != -1:
                                new_class_type_uuid = class_text_dict['TV Trailer']
                            else:
                                new_class_type_uuid = class_text_dict['TV Theme']
                    elif file_name.find('/extras/') != -1 or file_name.find('\\extras\\') != -1:
                        new_class_type_uuid = None
                    elif file_name.find('/backdrops/') != -1 or file_name.find('\\backdrops\\') != -1:
                        media_class_text = thread_db.MK_Server_Database_Media_Class_By_UUID(new_class_type_uuid)
                        if media_class_text == 'Movie':
                            if file_name.find('/theme.mp3') != -1 or file_name.find('/theme.mp4') != -1 or file_name.find('\\theme.mp3') != -1 or file_name.find('\\theme.mp4') != -1:
                                new_class_type_uuid = class_text_dict['Movie Theme']
                    # determine ffmpeg json data
                    if file_name[:1] == "\\":
                        file_name = file_name.replace('\\\\', 'smb://guest:\'\'@').replace('\\', '/')
                    media_ffprobe_json = MK_Common_FFMPEG.MK_Common_FFMPEG_Media_Attr(file_name)
                # create media_json data
                media_json = json.dumps({'DateAdded': datetime.now().strftime("%Y-%m-%d"), 'ChapterScan': True})
                media_id = str(uuid.uuid4())
                thread_db.MK_Server_Database_Insert_Media(media_id, file_name, new_class_type_uuid, None, media_ffprobe_json, media_json)
                # media id begin and download que insert
                thread_db.MK_Server_Database_Download_Insert('Z', json.dumps({'MediaID': media_id, 'Path': file_name, 'ClassID': new_class_type_uuid, 'Status': None, 'MetaNewID': str(uuid.uuid4()), 'ProviderMetaID': None}))
        total_scanned += 1
        thread_db.MK_Server_Database_Audit_Path_Update_Status(dir_guid, json.dumps({'Status': 'File scan: ' + locale.format('%d', total_scanned, True) + ' / ' + locale.format('%d', total_file_in_dir, True), 'Pct': (total_scanned / total_file_in_dir) * 100}))
        thread_db.MK_Server_Database_Commit()
    logging.info("Scan dir done: %s %s", dir_path, media_class_type_uuid)
    thread_db.MK_Server_Database_Audit_Path_Update_Status(dir_guid, None) # set to none so it doens't show up
    thread_db.MK_Server_Database_Commit()
    return total_files


def worker(audit_directory):
    data1, data2, dir_guid = audit_directory
    thread_db = database_base.MK_Server_Database()
    thread_db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())
    logging.debug('value=%s', data1)
    total_files = MK_Server_Media_Scan_Audit(thread_db, data1, data2, global_known_media, dir_guid, class_text_dict)
    if total_files > 0:
        thread_db.MK_Server_Database_Notification_Insert(locale.format('%d', total_files, True) + " file(s) added from " + data1, True)
    thread_db.MK_Server_Database_Commit()
    thread_db.MK_Server_Database_Close()
    return


if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# open the database
db = database_base.MK_Server_Database()
db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.MK_Server_Database_Activity_Insert(u'MediaKraken_Server File Scan Start', None, u'System: Server File Scan Start', u'ServerFileScanStart', None, None, u'System')


# load in all media from DB
global_known_media = []
known_media = db.MK_Server_Database_Known_Media()
# verify rows were returned
if known_media is not None:
    for media_row in known_media:
        global_known_media.append(media_row['mm_media_path'].encode('utf-8'))
known_media = None


# table the class_text into a dict...will lessen the db calls
class_text_dict = {}
for class_data in db.MK_Server_Database_Media_Class_List(None, None):
    class_text_dict[class_data['mm_media_class_type']] = class_data['mm_media_class_guid']
logging.debug('class: %s', class_text_dict)


# determine directories to audit
audit_directories = []
for row_data in db.MK_Server_Database_Audit_Paths():
    logging.info("Audit Path: %s", row_data)
    # check for UNC
    if row_data['mm_media_dir_path'][:1] == "\\":
        smb_stuff = MK_Common_CIFS.MK_Common_CIFS_Share_API()
        addr, share, path = MK_Common_String.UNC_To_Addr_Share_Path(row_data['mm_media_dir_path'])
        smb_stuff.MK_Common_CIFS_Connect(addr)
        if smb_stuff.MK_Common_CIFS_Share_Directory_Check(share, path):
            if datetime.strptime(time.ctime(smb_stuff.MK_Common_CIFS_Share_File_Dir_Info(share, path).last_write_time), "%a %b %d %H:%M:%S %Y") > row_data['mm_media_dir_last_scanned']:
                audit_directories.append((row_data['mm_media_dir_path'], str(row_data['mm_media_class_guid']), row_data['mm_media_dir_guid']))
                db.MK_Server_Database_Audit_Path_Update_Status(row_data['mm_media_dir_guid'], json.dumps({'Status': 'Added to scan', 'Pct': 100}))
        else:
            db.MK_Server_Database_Notification_Insert(('UNC Library path not found: %s', (row_data['mm_media_dir_path'],)), True)
        smb_stuff.MK_Common_CIFS_Close()
    else:
        if not os.path.isdir(row_data['mm_media_dir_path']): # make sure the path still exists
            db.MK_Server_Database_Notification_Insert(('Library path not found: %s', (row_data['mm_media_dir_path'],)), True)
        else:
            # verify the directory inodes has changed
            if datetime.strptime(time.ctime(os.path.getmtime(row_data['mm_media_dir_path'])), "%a %b %d %H:%M:%S %Y") > row_data['mm_media_dir_last_scanned']:
                audit_directories.append((row_data['mm_media_dir_path'], str(row_data['mm_media_class_guid']), row_data['mm_media_dir_guid']))
                db.MK_Server_Database_Audit_Path_Update_Status(row_data['mm_media_dir_guid'], json.dumps({'Status': 'Added to scan', 'Pct': 100}))


# commit
db.MK_Server_Database_Commit()


# start processing the directories
if len(audit_directories) > 0:
    # switched to this since tracebacks work this method
    with futures.ThreadPoolExecutor(len(audit_directories)) as executor:
        futures = [executor.submit(worker, n) for n in audit_directories]
        for future in futures:
            logging.debug(future.result())


# log end
db.MK_Server_Database_Activity_Insert(u'MediaKraken_Server File Scan Stop', None, u'System: Server File Scan Stop', u'ServerFileScanStop', None, None, u'System')


# commit
db.MK_Server_Database_Commit()


# close the database
db.MK_Server_Database_Close()


# remove pid
os.remove(pid_file)
