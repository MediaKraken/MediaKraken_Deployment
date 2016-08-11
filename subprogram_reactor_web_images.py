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
import logging
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import signal
import os
import sys
sys.path.append("../MediaKraken_Common")
import MK_Common_File
import MK_Common_Logging
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor
from twisted.internet import ssl

# create the file for pid
pid_file = './pid/' + str(os.getpid())
MK_Common_File.MK_Common_File_Save_Data(pid_file, 'Sub_Web_Image', False, False, None)


def signal_receive(signum, frame):
    print 'Web Image CHILD: Received USR1'
    # remove pid
    os.remove(pid_file)
    sys.stdout.flush()
    sys.exit(0)


# set signal breaks
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# start logging
MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Subprogram_Reactor_Web_Images')


# simple reactor to present images to clients
reactor.listenSSL(int(Config.get('MediaKrakenServer', 'ImageWeb').strip()), Site(File(Config.get('MediaKrakenServer', 'MetadataImageLocal').strip())), ssl.DefaultOpenSSLContextFactory('key/privkey.pem', 'key/cacert.pem'))
reactor.run()


# remove pid
os.remove(pid_file)
