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
from common import common_logging
from common import common_signal
import subprocess
import time
from multiprocessing import Process
from os import path
from twisted.internet import reactor, protocol, stdio, defer, task
from twisted.protocols import basic
from network import network_base_line_ripper as network_base

class MediaKrakenServerApp(protocol.ServerFactory):
    def __init__(self):
        # start logging
        common_logging.com_logging_start('./log/MediaKraken_Subprogram_Reactor_Line')
        # set other data
        self.server_start_time = time.mktime(time.gmtime())
        self.users = {} # maps user names to network instances
        logging.info("Ready for connections!")


    def buildProtocol(self, addr):
        return network_base.NetworkEvents(self.users, self.db_connection)


if __name__ == '__main__':
    # set signal exit breaks
    common_signal.com_signal_set_break()
    # setup for the ssl keys
    reactor.listenTCP(5000, MediaKrakenServerApp())
    reactor.run()

'''
# Rip drive to FLAC using abcde
def begin_rip(directory):
    drive_loc = '/dev/' + directory.split('=')[-1]
    # Continuous loop to search for newly entered discs
    while True:
        if path.exists(directory): # Checks if an audio disc has been entered
            print('Found disc in drive ', drive_loc)
            subprocess.call(['abcde','-d', drive_loc]) # Run abcde with drive
            print('Finished processing disc in drive ', drive_loc)
        time.sleep(5)

# These directories will need to change based on where your cd's mount
d1 = Process(target=begin_rip, args=('/run/user/1000/gvfs/cdda:host=sr0',))
d2 = Process(target=begin_rip, args=('/run/user/1000/gvfs/cdda:host=sr1',))
d3 = Process(target=begin_rip, args=('/run/user/1000/gvfs/cdda:host=sr2',))

d1.start()
d2.start()
d3.start()
'''
