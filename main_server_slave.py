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
import os
import platform
import subprocess
import json
from threading import Event, Thread
import sys
import uuid
from common import common_celery
from common import common_logging
from common import common_network_share
from common import common_signal
from common import common_system
from common import common_version
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor, protocol
from twisted.internet import ssl

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        #self.factory.app.on_connection(self.transport)
        pass

    def dataReceived(self, data):
        """
        Process network message from server
        """
        json_message = json.loads(data)
        if json_message['Type'] != "IMAGE":
            logging.info("Got Message: %s", data)
        logging.info("len total: %s", len(data))

        msg = None
        if json_message['Type'] == "Ident":
            msg = json.dumps({'Type': 'Ident', 'UUID': str(uuid.uuid4()),
                'Platform': platform.node()}).encode("utf8")
        elif json_message['Type'] == "Play":
            if json_message['Sub'] == 'Cast':
                if json_message['Command'] == "Chapter Back":
                    pass
                elif json_message['Command'] == "Chapter Forward":
                    pass
                elif json_message['Command'] == "Fast Forward":
                    pass
                elif json_message['Command'] == "Mute":
                    subprocess.Popen(('python', '/mediakraken/stream2chromecast/stream2chromecast.py',
                                      '-devicename', json_message['Device'], '-mute'), shell=False)
                elif json_message['Command'] == "Pause":
                    subprocess.Popen(('python', '/mediakraken/stream2chromecast/stream2chromecast.py',
                                      '-devicename', json_message['Device'], '-pause'), shell=False)
                elif json_message['Command'] == 'Play':
                    # should only need to check for subs on initial play command
                    if 'Subtitle' in json_message:
                        subtitle_command = ('-subtitles', json_message['Subtitle'],
                                            '-subtitles_language', json_message['Language'])
                    else:
                        subtitle_command = ()
                    subprocess.Popen(('python', '/mediakraken/stream2chromecast/stream2chromecast.py',
                        '-devicename', json_message['Device'],
                        subtitle_command, '-transcodeopts', '-c:v', 'copy', '-c:a', 'ac3',
                        '-movflags', 'faststart+empty_moov',
                        '-transcode', json_message['Data']), shell=False)
                elif json_message['Command'] == "Rewind":
                    pass
                elif json_message['Command'] == 'Stop':
                    subprocess.Popen(('python', '/mediakraken/stream2chromecast/stream2chromecast.py',
                                      '-devicename', json_message['Device'], '-stop'), shell=False)
                elif json_message['Command'] == "Volume Down":
                    subprocess.Popen(('python', '/mediakraken/stream2chromecast/stream2chromecast.py',
                                      '-devicename', json_message['Device'], '-voldown'), shell=False)
                elif json_message['Command'] == "Volume Set":
                    subprocess.Popen(('python', '/mediakraken/stream2chromecast/stream2chromecast.py',
                                      '-devicename', json_message['Device'], '-setvol', json_message['Data']),
                                      shell=False)
                elif json_message['Command'] == "Volume Up":
                    subprocess.Popen(('python', '/mediakraken/stream2chromecast/stream2chromecast.py',
                                      '-devicename', json_message['Device'], '-volup'), shell=False)
            elif json_message['Sub'] == 'HDHomeRun':
                pass
            elif json_message['Sub'] == 'Slave':
                if json_message['Command'] == "Chapter Back":
                    pass
                elif json_message['Command'] == "Chapter Forward":
                    pass
                elif json_message['Command'] == "Fast Forward":
                    pass
                elif json_message['Command'] == "Pause":
                    pass
                elif json_message['Command'] == 'Play':
                    self.proc_ffmpeg_stream = subprocess.Popen((''), shell=False)
                elif json_message['Command'] == "Rewind":
                    pass
                elif json_message['Command'] == 'Stop':
                    os.killpg(self.proc_ffmpeg_cast)
        elif json_message['Type'] == "System":
            if json_message['Sub'] == 'CPU':
                msg = json.dumps({'Type': 'System', 'Sub': 'CPU',
                                  'Data': common_system.com_system_cpu_usage(False)})
            elif json_message['Sub'] == "Disk":
                msg = json.dumps({'Type': 'System', 'Sub': 'Disk',
                                  'Data': common_system.com_system_disk_usage_all(True)})
            elif json_message['Sub'] == "MEM":
                msg = json.dumps({'Type': 'System', 'Sub': 'MEM',
                                  'Data': common_system.com_system_virtual_memory(False)})
            elif json_message['Sub'] == "SYS":
                msg = json.dumps({'Type': 'System', 'Sub': 'SYS',
                                  'Data': common_system.com_system_cpu_usage(True),
                                  'Data2': common_system.com_system_disk_usage_all(True),
                                  'Data3': common_system.com_system_virtual_memory(False)})
        else:
            logging.error("Unknown message type")
        if msg is not None:
            logging.info("should be sending data")
            self.transport.write(msg.encode("utf8"))


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        #self.app.print_message("connection lost")
        logging.info('connection lost')

    def clientConnectionFailed(self, conn, reason):
        #self.app.print_message("connection failed")
        logging.info('connection failed')


class MediaKrakenApp():

    def exit_program(self):
        pass

    def build(self):
        root = MediaKrakenApp()
        self.connect_to_server()
        return root

    def connect_to_server(self):
        """
        Connect to media server
        """
        reactor.connectSSL('mkserver', 8903,
                           EchoFactory(self), ssl.ClientContextFactory())
        reactor.run()

if __name__ == '__main__':
    # start logging
    common_logging.com_logging_start('./log/MediaKraken_Slave')
    # set signal exit breaks
    common_signal.com_signal_set_break()
    MediaKrakenApp().build()
