"""
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
"""

import datetime
import shlex
import subprocess

from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch
from common import common_signal

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_streamlink')
# set signal exit breaks
common_signal.com_signal_set_break()
# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# do the actual capture
filename = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + user + " - " \
           + (info['stream']).get("channel").get("status") + ".flv"
filename = format_filename(filename)
subprocess.call(shlex.split('./bin/streamlink twitch.tv/' + user + quality,
                            '-o \"' + filename + '\"'))

# commit all changes
db_connection.db_commit()

# close the database
db_connection.db_close()
