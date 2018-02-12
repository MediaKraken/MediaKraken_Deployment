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
import logging  # pylint: disable=W0611
from common import common_config_ini
from common import common_file
from common import common_internationalization
from common import common_logging
from common import common_metadata_chart_lyrics
from common import common_signal

# set signal exit breaks
common_signal.com_signal_set_break()

# start logging
common_logging.com_logging_start(
    './log/MediaKraken_Subprogram_Lyrics_Download')

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

total_download_attempts = 0
# main code
# parse arguments
sub_lang = "en"
# search the directory for filter files
for media_row in common_file.com_file_dir_list():
    logging.info(media_row)

print('Total lyrics download attempts: %s' % total_download_attempts)
# send notifications
if total_download_attempts > 0:
    db_connection.db_notification_insert(
        common_internationalization.com_inter_number_format(
            total_download_attempts)
        + " lyric(s) downloaded.", True)

# commit all changes
db_connection.db_commit()

# close DB
db_connection.db_close()
