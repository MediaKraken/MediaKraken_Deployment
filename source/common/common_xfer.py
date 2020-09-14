"""
Threads for transfering files
"""

import socket
import struct
import threading
import time

from . import common_global


def getallbytes(con, bytesleft):
    """
    Read bytes in the connection buffer
    """
    return_buffer = ""
    while bytesleft:
        data = con.recv(bytesleft)
        bytesleft -= len(data)
        return_buffer += data
    return return_buffer


class FileSenderThread(threading.Thread):
    """
    Thread for sending a file
    """

    def __init__(self, targetip, targetport, filenames, filelocations):
        self.host = targetip
        self.port = targetport
        self.filenames = filenames
        self.filelocations = filelocations
        threading.Thread.__init__(self)

    def run(self):
        try:
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.settimeout(60.0)
            clientsocket.connect((self.host, self.port))
            for fileindex in range(0, len(self.filenames)):
                data = open(self.filelocations[fileindex], 'rb').read()
                common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {"fn": self.filenames[fileindex],
                                                                 'types': type(
                                                                     self.filenames[fileindex])})
                clientsocket.sendall(b"FILE" + struct.pack("<i256s", len(data),
                                                           str(self.filenames[fileindex])))
                for ndx in range(0, (len(data) + 1023) / 1024):
                    clientsocket.sendall(data[ndx * 1024:(ndx + 1) * 1024])
                    time.sleep(0.05)
            clientsocket.sendall(b'FEND')
            clientsocket.close()
        except socket.error as msg:
            common_global.es_inst.com_elastic_index('error', {'Sending files failed.':
                                                                  str(msg)})


class FileReceiverThread(threading.Thread):
    """
    Thread for receiving files
    """

    def __init__(self, receive_port):
        threading.Thread.__init__(self)
        self.filedone = 0
        self.filesize = 1
        self.receive_port = receive_port

    def run(self):
        try:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'Listening for response on port':
                                                                 self.receive_port})
            localsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            localsocket.settimeout(60.0)
            localsocket.bind(('', self.receive_port))
            localsocket.listen(1)
            con, addr = localsocket.accept()
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'Connection address': addr})
            con.settimeout(60.0)
            while True:
                data = getallbytes(con, 4)
                if not data:
                    break
                elif data == 'FEND':
                    break
                elif data == 'FILE':
                    data = getallbytes(con, 260)
                    self.filesize, filename = struct.unpack("<i256s", data)
                    filename = filename.replace('\0', '')
                    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'size': self.filesize,
                                                                     'name': filename})
                    filename = str(filename)
                    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'filename': filename})
                    file_handle = open('../roms/' + filename, 'wb')
                    fileleft = self.filesize
                    while fileleft:
                        data = con.recv(min(fileleft, 1024))
                        fileleft = max(0, fileleft - len(data))
                        self.filedone = self.filesize - fileleft
                        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
                                                                {'percent done':
                                                                     self.filedone * 100 / self.filesize})
                        file_handle.write(data)
                    file_handle.close()
                    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'stuff': 'file finished'})
                else:
                    raise Exception('ERROR GETTING FILES (NO FILE OR FEND)')
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
                                                    {'stuff': 'Finished getting all files!'})
            del localsocket
        except socket.error as msg:
            common_global.es_inst.com_elastic_index('error', {"Transfer Failed": str(msg)})
