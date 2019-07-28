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

import json
import os
import shlex
import socket
import subprocess
import time

from . import common_global


# https://mpv.io/manual/master/#json-ipc
class CommonNetMPVSocat:
    def __init__(self, sockfile='./mk_mpv.sock'):
        # allow time for mpv to setup the socket
        while True:
            time.sleep(0.1)
            try:
                self.socket_stream = socket.socket(
                    socket.AF_UNIX, socket.SOCK_STREAM)
                self.socket_stream.connect(sockfile)
            except socket.error as sock_err:
                if (sock_err.errno == socket.errno.ECONNREFUSED):
                    print("Connection was refused")
                    continue
            except OSError as e:
                # if e.errno == e.ENOENT:
                #     # do your FileNotFoundError code here
                print("File not found")
                continue
            else:
                break
        # close connection since I'm using socat
        self.socket_stream.close()
        self.sockfile = sockfile

    def execute(self, command):
        self.sub_output = subprocess.Popen(
            shlex.split('echo \'' + command + '\' | socat - ' + self.sockfile),
            stdout=subprocess.PIPE, stderr=None, shell=True)
        output = self.sub_output.communicate()
        print(('subout: ', output))

    def close(self):
        os.remove(self.sockfile)


class CommonNetMPV:
    def __init__(self, sockfile='./mk_mpv.sock'):
        # allow time for mpv to setup the socket
        while True:
            time.sleep(0.1)
            try:
                self.socket_stream = socket.socket(
                    socket.AF_UNIX, socket.SOCK_STREAM)
                self.socket_stream.connect(sockfile)
            except socket.error as sock_err:
                if (sock_err.errno == socket.errno.ECONNREFUSED):
                    print("Connection was refused")
                    continue
            except OSError as e:
                # if e.errno == e.ENOENT:
                #     # do your FileNotFoundError code here
                print("File not found")
                continue
            else:
                break
        # self.sockfile = sockfile

    def execute(self, command):
        self.socket_stream.sendall(command.encode('utf-8'))
        result = json.loads(self.socket_stream.recv(1024).decode('utf-8'))
        common_global.es_inst.com_elastic_index('info', {'mpv result': result})
        if result['error'] == 'success':
            return result

    def close(self):
        self.socket_stream.close()
        # os.remove(self.sockfile)
