import os
import os.path
import socket
import json
from functools import partial


class Error(Exception):
    pass

class SocketError(Error):
    pass

class MpvError(Error):
    pass

class Mpv(object):
    commands = ['']
    def __init__(self, sockfile='/tmp/mpvsock'):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            s.connect(sockfile)
        except OSError as e:
            raise SocketError from e
        self.fd = s

    def execute(self, command):
        data = json.dumps(command) + '\r\n'
        data = bytes(data, encoding='utf-8')
        try:
            self.fd.send(data)
            buf = self.fd.recv(1024)
        except OSError as e:
            raise SocketError from e
        print('DEBUG', buf)
        result = json.loads(buf.decode('utf-8'))
        status = result['error']
        if status == 'success': 
            return result
        raise MpvError(status)

    def command(self, command, *args):
        return self.execute({'command': [command, *args]})

    def close(self):
        self.fd.close()

    def __getattr__(self, name):
        mpv_name = name.replace('_', '-')
        return partial(self.command, mpv_name)

