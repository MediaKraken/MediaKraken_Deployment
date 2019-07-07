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

import os
import subprocess

from build_image_directory import build_image_dirs
from build_trailer_directory import build_trailer_dirs
from common import common_global
from common import common_logging_elasticsearch
from common import common_metadata_limiter
from common import common_network
from common import common_signal

# TODO should be using env variables
# build image directories if needed
if not os.path.isdir('/mediakraken/web_app/MediaKraken/static/meta/images/backdrop/a'):
    build_image_dirs()

# TODO should be using env variables
# build trailer directories if needed
if not os.path.isdir('/mediakraken/web_app/MediaKraken/static/meta/trailers/trailer/a'):
    build_trailer_dirs()

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('main_metadata_api')

# set signal exit breaks
common_signal.com_signal_set_break()

# fire off wait for it script to allow rabbitmq connection
# doing here so I don't have to do it multiple times
common_network.mk_network_service_available('mkrabbitmq', '5672')

# fire up the workers for each provider
for meta_provider in list(common_metadata_limiter.API_LIMIT.keys()):
    common_global.es_inst.com_elastic_index('info', {'meta_provider': meta_provider})
    proc_api_fetch = subprocess.Popen(['python3', './main_server_metadata_api_worker.py',
                                       meta_provider], stdout=subprocess.PIPE, shell=False)
# TODO this only wait for the last one......so, if that bombs....could kill rest on exit
proc_api_fetch.wait()  # so this doesn't end which will cause docker to restart
