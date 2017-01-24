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
from common import common_config_ini
from common import common_logging
from common import common_signal
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.static import File
from twisted.internet import ssl


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Reactor_Web_Images')


option_config_json, db_connection = common_config_ini.com_config_read()


# read in paths to add to reactor
root = Resource()
root.putChild('prox-1', File(option_config_json['MediaKrakenServer']['MetadataImageLocal']))
for row_data in db_connection.db_audit_paths():
    root.putChild('prox-' + row_data['mm_media_dir_guid'],
        File(row_data['mm_media_dir_path']))
# create and launch reactor
reactor.listenSSL(5001 , Site(root),
    ssl.DefaultOpenSSLContextFactory('key/privkey.pem', 'key/cacert.pem'))
reactor.run()
