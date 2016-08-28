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
import signal
import os
import sys
from common import common_config_ini
from common import common_file
from common import common_logging
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor
from twisted.internet import ssl

# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'Sub_Web_Image', False, False, None)


def signal_receive(signum, frame): # pylint: disable=W0613
    """
    Handle signal interupt
    """
    print('Web Image CHILD: Received USR1')
    # remove pid
    os.remove(pid_file)
    sys.stdout.flush()
    sys.exit(0)


# set signal breaks
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c # pylint: disable=E1101
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Reactor_Web_Images')

config_handle, option_config_json, db_connection = common_config_ini.com_config_read()
# simple reactor to present images to clients
reactor.listenSSL(int(option_config_json['MediaKrakenServer']['ImageWeb']),\
    Site(File(option_config_json['MediaKrakenServer']['MetadataImageLocal'])),\
    ssl.DefaultOpenSSLContextFactory('key/privkey.pem', 'key/cacert.pem'))
reactor.run()


# remove pid
os.remove(pid_file)
