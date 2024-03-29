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

import sys

from common import common_file
from common import common_logging_elasticsearch_httpx
from common import common_network
from common import common_signal
from common import common_system

# verify this program isn't already running!
if common_system.com_process_list(
        process_name='/usr/bin/python3 /mediakraken/subprogram_games_libretro_core.py'):
    sys.exit(0)

# start logging
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text='START',
                                                     index_name='subprogram_games_libreto_core')

# set signal exit breaks
common_signal.com_signal_set_break()

# populate current cores
libretro_current_core = common_file.com_file_dir_list('/mediakraken/emulation/cores',
                                                      filter_text=None, walk_dir=None,
                                                      skip_junk=False, file_size=False,
                                                      directory_only=False,
                                                      file_modified=True)

libtro_url = 'http://buildbot.libretro.com/nightly/linux/x86_64/latest/'
# date md5 core_filename.zip
for libretro_core in common_network.mk_network_fetch_from_url(libtro_url
                                                              + '.index-extended').split('\n'):
    download_core = False
    core_date, core_md5, core_name = libretro_core.split(' ')
    if core_name in libretro_current_core:
        # we have the core, check to see if it's newer
        if libretro_current_core[core_name] < core_date.replace('-', ''):
            download_core = True
    else:
        download_core = True
    if download_core:
        # download the missing or newer core
        common_network.mk_network_fetch_from_url(libtro_url + core_name,
                                                 '/mediakraken/emulation/cores/' + core_name)
        # unzip the core for use
        common_file.com_file_unzip('/mediakraken/emulation/cores/' + core_name,
                                   target_destination_directory=None, remove_zip=True)
