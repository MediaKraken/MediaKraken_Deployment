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
from datetime import datetime # to handle threading
import os
import uuid
import time
import json
import locale
locale.setlocale(locale.LC_ALL, '')
from concurrent import futures
from common import common_config_ini
from common import common_network_cifs
from common import common_ffmpeg
from common import common_file
from common import common_file_extentions
from common import common_logging
from common import common_signal
from common import common_string
#lock = threading.Lock()


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_File_Scan')


def worker(audit_directory):
    """
    Worker thread for each directory
    """
    dir_path, media_class_type_uuid, dir_guid = audit_directory
    # open the database
    config_handle, option_config_json, thread_db = common_config_ini.com_config_read()
    logging.info('value=%s', dir_path)
    # update the timestamp now so any other media added DURING this scan don't get skipped
    thread_db.db_audit_dir_timestamp_update(dir_path)
    thread_db.db_audit_path_update_status(dir_guid,\
        json.dumps({'Status': 'File search scan', 'Pct': 0}))
    thread_db.db_commit()
    # check for UNC before grabbing dir list
    if dir_path[:1] == "\\":
        file_data = []
        smb_stuff = common_network_cifs.CommonCIFSShare()
        addr, share, path = common_string.com_string_unc_to_addr_path(dir_path)
        smb_stuff.com_cifs_connect(addr)
        for dir_data in smb_stuff.com_cifs_walk(share, path):
            for file_name in dir_data[2]:
                file_data.append('\\\\' + addr + '\\' + share + '\\' + dir_data[0]\
                    + '\\' + file_name)
        smb_stuff.com_cifs_close()
    else:
        file_data = common_file.com_file_dir_list(dir_path, None, True, False)
    total_file_in_dir = len(file_data)
    total_scanned = 0
    total_files = 0
    for file_name in file_data:
        # TODO whined about converting both to utf8
        if file_name in global_known_media:
            pass # already scanned, skip
        else:
            filename_base, file_extension = os.path.splitext(file_name)
            if file_extension[1:].lower() in common_file_extentions.MEDIA_EXTENSION\
                    or file_extension[1:].lower() in common_file_extentions.SUBTITLE_EXTENSION:
                save_dl_record = True
                # check for "stacked" media file
                head, base_file_name = os.path.split(file_name)
                if common_string.STACK_CD.search(base_file_name) is not None\
                        or common_string.STACK_PART.search(base_file_name) is not None\
                        or common_string.STACK_DVD.search(base_file_name) is not None\
                        or common_string.STACK_PT.search(base_file_name) is not None\
                        or common_string.STACK_DISK.search(base_file_name) is not None\
                        or common_string.STACK_DISC.search(base_file_name) is not None:
                    # check to see if it's part one or not
                    if common_string.STACK_CD1.search(base_file_name) is None\
                            and common_string.STACK_PART1.search(base_file_name) is None\
                            and common_string.STACK_DVD1.search(base_file_name) is None\
                            and common_string.STACK_PT1.search(base_file_name) is None\
                            and common_string.STACK_DISK1.search(base_file_name) is None\
                            and common_string.STACK_DISC1.search(base_file_name) is None:
                        # it's not a part one here so, no DL record needed
                        save_dl_record = False
                total_files += 1
                filename_base, file_extension = os.path.splitext(file_name)
                new_class_type_uuid = media_class_type_uuid
                # video game data, don't do ffmpeg
                if thread_db.db_media_class_by_uuid(media_class_type_uuid) == 'Video Game':
                    if file_extension.lower() == 'iso':
                        new_class_type_uuid = class_text_dict['Game ISO']
                    elif file_extension.lower() == 'chd':
                        new_class_type_uuid = class_text_dict['Game CHD']
                    else:
                        new_class_type_uuid = class_text_dict['Game ROM']
                    # TODO lookup game info in game database data
                    media_ffprobe_json = None
                # if an extention skip
                elif file_extension.lower() in common_file_extentions.MEDIA_EXTENSION_SKIP_FFMPEG\
                        or file_extension.lower() in common_file_extentions.SUBTITLE_EXTENSION:
                    media_ffprobe_json = None
                    if file_extension.lower() in common_file_extentions.SUBTITLE_EXTENSION:
                        new_class_type_uuid = class_text_dict['Subtitle']
                else:
                    if file_name.find('/trailers/') != -1\
                            or file_name.find('\\trailers\\') != -1\
                            or file_name.find('/theme.mp3') != -1\
                            or file_name.find('\\theme.mp3') != -1\
                            or file_name.find('/theme.mp4') != -1\
                            or file_name.find('\\theme.mp4') != -1:
                        media_class_text = thread_db.db_media_class_by_uuid(new_class_type_uuid)
                        if media_class_text == 'Movie':
                            if file_name.find('/trailers/') != -1\
                                    or file_name.find('\\trailers\\') != -1:
                                new_class_type_uuid = class_text_dict['Movie Trailer']
                            else:
                                new_class_type_uuid = class_text_dict['Movie Theme']
                        elif media_class_text == 'TV Show' or media_class_text == 'TV Episode'\
                                or media_class_text == 'TV Season':
                            if file_name.find('/trailers/') != -1\
                                    or file_name.find('\\trailers\\') != -1:
                                new_class_type_uuid = class_text_dict['TV Trailer']
                            else:
                                new_class_type_uuid = class_text_dict['TV Theme']
                    elif file_name.find('/extras/') != -1 or file_name.find('\\extras\\') != -1:
                        if media_class_text == 'Movie':
                            new_class_type_uuid = class_text_dict['Movie Extras']
                        elif media_class_text == 'TV Show' or media_class_text == 'TV Episode'\
                                or media_class_text == 'TV Season':
                            new_class_type_uuid = class_text_dict['TV Extras']
                    elif file_name.find('/backdrops/') != -1\
                            or file_name.find('\\backdrops\\') != -1:
                        media_class_text = thread_db.db_media_class_by_uuid(new_class_type_uuid)
                        if media_class_text == 'Movie':
                            if file_name.find('/theme.mp3') != -1\
                                    or file_name.find('\\theme.mp3') != -1\
                                    or file_name.find('/theme.mp4') != -1\
                                    or file_name.find('\\theme.mp4') != -1:
                                new_class_type_uuid = class_text_dict['Movie Theme']
                    # determine ffmpeg json data
                    if file_name[:1] == "\\":
                        file_name\
                            = file_name.replace('\\\\', 'smb://guest:\'\'@').replace('\\', '/')
                    media_ffprobe_json = common_ffmpeg.com_ffmpeg_media_attr(file_name)
                # create media_json data
                media_json = json.dumps({'DateAdded': datetime.now().strftime("%Y-%m-%d"),\
                    'ChapterScan': True})
                media_id = str(uuid.uuid4())
                thread_db.db_insert_media(media_id, file_name,\
                    new_class_type_uuid, None, media_ffprobe_json, media_json)
                if save_dl_record:
                    # media id begin and download que insert
                    thread_db.db_download_insert('Z', json.dumps({'MediaID': media_id,\
                        'Path': file_name, 'ClassID': new_class_type_uuid, 'Status': None,\
                        'MetaNewID': str(uuid.uuid4()), 'ProviderMetaID': None}))
        total_scanned += 1
        thread_db.db_audit_path_update_status(dir_guid,\
            json.dumps({'Status': 'File scan: ' + locale.format('%d', total_scanned, True)\
            + ' / ' + locale.format('%d', total_file_in_dir, True),\
            'Pct': (total_scanned / total_file_in_dir) * 100}))
        thread_db.db_commit()
    logging.info("Scan dir done: %s %s", dir_path, media_class_type_uuid)
    thread_db.db_audit_path_update_status(dir_guid, None) # set to none so it doens't show up
    if total_files > 0:
        thread_db.db_notification_insert(locale.format('%d', total_files, True)\
            + " file(s) added from " + dir_path, True)
    thread_db.db_commit()
    thread_db.db_close()
    return


# open the database
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server File Scan Start', None,\
    'System: Server File Scan Start', 'ServerFileScanStart', None, None, 'System')


# load in all media from DB
global_known_media = [] # pylint: disable=C0103
known_media = db_connection.db_known_media()
# verify rows were returned
if known_media is not None:
    for media_row in known_media:
        global_known_media.append(media_row['mm_media_path'].encode('utf-8'))
known_media = None


# table the class_text into a dict...will lessen the db calls
class_text_dict = {}
for class_data in db_connection.db_media_class_list(None, None):
    class_text_dict[class_data['mm_media_class_type']] = class_data['mm_media_class_guid']
logging.info('class: %s', class_text_dict)


# determine directories to audit
audit_directories = [] # pylint: disable=C0103
for row_data in db_connection.db_audit_paths():
    logging.info("Audit Path: %s", row_data)
    # check for UNC
    if row_data['mm_media_dir_path'][:1] == "\\":
        smb_stuff = common_network_cifs.CommonCIFSShare()
        addr, share, path\
            = common_string.com_string_unc_to_addr_path(row_data['mm_media_dir_path'])
        smb_stuff.com_cifs_connect(addr)
        if smb_stuff.com_cifs_share_directory_check(share, path):
            if datetime.strptime(time.ctime(\
                    smb_stuff.com_cifs_share_file_dir_info(share, path).last_write_time),\
                    "%a %b %d %H:%M:%S %Y") > row_data['mm_media_dir_last_scanned']:
                audit_directories.append((row_data['mm_media_dir_path'],\
                    str(row_data['mm_media_class_guid']), row_data['mm_media_dir_guid']))
                db_connection.db_audit_path_update_status(row_data['mm_media_dir_guid'],\
                    json.dumps({'Status': 'Added to scan', 'Pct': 100}))
        else:
            db_connection.db_notification_insert('UNC Library path not found: %s'\
                % row_data['mm_media_dir_path'], True)
        smb_stuff.com_cifs_close()
    else:
        if not os.path.isdir(row_data['mm_media_dir_path']): # make sure the path still exists
            db_connection.db_notification_insert('Library path not found: %s'\
                % row_data['mm_media_dir_path'], True)
        else:
            # verify the directory inodes has changed
            if datetime.strptime(time.ctime(os.path.getmtime(row_data['mm_media_dir_path'])),\
                    "%a %b %d %H:%M:%S %Y") > row_data['mm_media_dir_last_scanned']:
                audit_directories.append((row_data['mm_media_dir_path'],\
                    str(row_data['mm_media_class_guid']), row_data['mm_media_dir_guid']))
                db_connection.db_audit_path_update_status(row_data['mm_media_dir_guid'],\
                    json.dumps({'Status': 'Added to scan', 'Pct': 100}))


# commit
db_connection.db_commit()


# start processing the directories
if len(audit_directories) > 0:
    # switched to this since tracebacks work this method
    with futures.ThreadPoolExecutor(len(audit_directories)) as executor:
        futures = [executor.submit(worker, n) for n in audit_directories]
        for future in futures:
            logging.info(future.result())


# log end
db_connection.db_activity_insert('MediaKraken_Server File Scan Stop', None,\
    'System: Server File Scan Stop', 'ServerFileScanStop', None, None, 'System')


# commit
db_connection.db_commit()


# close the database
db_connection.db_close()
