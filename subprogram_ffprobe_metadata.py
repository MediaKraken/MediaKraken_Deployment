'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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
import sys
from common import common_config_ini
from common import common_ffmpeg
from common import common_logging

# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_FFPROBE_Scan')

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

db_connection.db_media_ffmeg_update(sys.argv[1],
                                    json.dumps(common_ffmpeg.com_ffmpeg_media_attr(
                                    db_connection.db_read_media(sys.argv[1])['mm_media_path'])))

# commit
db_connection.db_commit()

# close the database
db_connection.db_close()
