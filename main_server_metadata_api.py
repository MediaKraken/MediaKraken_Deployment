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
import os
import subprocess
from build_image_directory import build_image_dirs
from common import common_metadata_limiter
from common import common_signal


# build image directories if needed
if os.path.isdir('/mediakraken/web_app/MediaKraken/static/meta/images/backdrop/a'):
    pass
else:
    build_image_dirs()


# set signal exit breaks
common_signal.com_signal_set_break()


# fire up the image downloader
proc_image_fetch = subprocess.Popen(['python', './main_server_metadata_api_worker_image.py'], \
                                    shell=False)
# fire up the workers for each provider
for meta_provider in common_metadata_limiter.API_LIMIT.keys():
    proc_api_fetch = subprocess.Popen(['python', './main_server_metadata_api_worker.py', \
                                       meta_provider], shell=False)
