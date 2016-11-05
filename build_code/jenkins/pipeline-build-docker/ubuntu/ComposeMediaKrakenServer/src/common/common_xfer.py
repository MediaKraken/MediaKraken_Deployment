"""
Threads for transfering files
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import socket
import threading
import struct
import time


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
            for fileindex in xrange(0, len(self.filenames)):
                data = open(self.filelocations[fileindex], 'rb').read()
                logging.info("fn: %s %s", self.filenames[fileindex],\
                    type(self.filenames[fileindex]))
                clientsocket.sendall("FILE"+struct.pack("<i256s", len(data),\
                    str(self.filenames[fileindex])))
                for ndx in xrange(0, (len(data)+1023)/1024):
                    clientsocket.sendall(data[ndx*1024:(ndx+1)*1024])
                    time.sleep(0.05)
            clientsocket.sendall('FEND')
            clientsocket.close()
        except socket.error, msg:
            logging.error('Sending files failed. %s', str(msg))


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
            logging.info('Listening for response on port %s', self.receive_port)
            localsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            localsocket.settimeout(60.0)
            localsocket.bind(('', self.receive_port))
            localsocket.listen(1)
            con, addr = localsocket.accept()
            logging.info('Connection address: %s', addr)
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
                    logging.info("%s %s", self.filesize, filename)
                    filename = str(filename)
                    logging.info('filename %s', filename)
                    file_handle = open('../roms/' + filename, 'wb')
                    fileleft = self.filesize
                    while fileleft:
                        data = con.recv(min(fileleft, 1024))
                        fileleft = max(0, fileleft - len(data))
                        self.filedone = self.filesize - fileleft
                        logging.info('percent done %s', self.filedone * 100 / self.filesize)
                        file_handle.write(data)
                    file_handle.close()
                    logging.info('file finished')
                else:
                    raise Exception('ERROR GETTING FILES (NO FILE OR FEND)')
            logging.info('Finished getting all files!')
            del localsocket
        except socket.error as msg:
            logging.error("Transfer Failed: %s", str(msg))
