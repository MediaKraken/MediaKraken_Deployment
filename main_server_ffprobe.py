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
import json
import time
from common import common_config_ini
from common import common_logging
from common import common_ffmpeg
from common import common_signal


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_FFPROBE')


# open the database
option_config_json, db_connection = common_config_ini.com_config_read()


# main code
while 1:
    for row_data in db_connection.db_read_media_ffprobe():
        ffprobe_json = common_ffmpeg.com_ffmpeg_media_attr(row_data['mm_media_path'])
        if ffprobe_json is not None:
            # update record with new ffprobe data
            pass # below is the update using the json returned above
        else:
            # update record with "hold" item
            ffprobe_json = {'FFProbe': 'Fail'}
        db_connection.db_media_ffmeg_update(row_data['mm_media_guid'], json.dumps(ffprobe_json))
    time.sleep(1)
