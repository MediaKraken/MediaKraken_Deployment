"""
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
"""

import os
import shlex
import subprocess
import sys

from common import common_config_ini
from common import common_file
from common import common_logging_elasticsearch_httpx
from common import common_signal
from common import common_system

# verify this program isn't already running!
if common_system.com_process_list(
        process_name='/usr/bin/python3 /mediakraken/subprogram_metadata_subtitle_downloader.py'):
    sys.exit(0)

# start logging
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text='START',
                                                     index_name='subprogram_metadata_subtitle_downloader')

# set signal exit breaks
common_signal.com_signal_set_break()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

total_download_attempts = 0

# parse arguments
sub_lang = "en"
# loop through all the libraries
for lib_row in db_connection.db_library_paths():
    # search the directory for filter files
    for media_row in common_file.com_file_dir_list(lib_row['mm_media_dir_path'],
                                                   ('avi', 'mkv', 'mp4', 'm4v'), True):
        # run the subliminal fetch for episode
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'title check': media_row.rsplit(
                '.', 1)[0] + "." + sub_lang + ".srt"})
        # not os.path.exists(media_row.rsplit('.',1)[0] + ".en.srt")
        # and not os.path.exists(media_row.rsplit('.',1)[0] + ".eng.srt")
        if not os.path.exists(media_row.rsplit('.', 1)[0] + "." + sub_lang + ".srt"):
            # change working dir so srt is saved in the right spot
            total_download_attempts += 1
            os.chdir(media_row.rsplit('/', 1)[0])
            file_handle = subprocess.Popen(shlex.split(
                "subliminal -l " + sub_lang + " -- \"" + media_row + "\""),
                stdout=subprocess.PIPE, shell=False)
            cmd_output = file_handle.communicate()[0]
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
                'Download Status': cmd_output})

# TODO put in the notifications
print(('Total subtitle download attempts: %s' % total_download_attempts), flush=True)

# close DB
db_connection.db_close()
