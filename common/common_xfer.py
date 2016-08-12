from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import socket
import threading
import struct
import time


def getAllBytes(con, bytesLeft):
    return_buffer = ""
    while bytesLeft:
        data = con.recv(bytesLeft)
        bytesLeft -= len(data)
        return_buffer += data
    return return_buffer


class FileSenderThread(threading.Thread):
    def __init__(self, targetIP, targetPort, fileNames, fileLocations):
        self.host = targetIP
        self.port = targetPort
        self.fileNames = fileNames
        self.fileLocations = fileLocations
        threading.Thread.__init__(self)


    def run(self):
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.settimeout(60.0)
            clientSocket.connect((self.host, self.port))
            for fileindex in xrange(0, len(self.fileNames)):
                data = open(self.fileLocations[fileindex], 'rb').read()
                logging.debug("fn: %s %s", self.fileNames[fileindex],\
                    type(self.fileNames[fileindex]))
                clientSocket.sendall("FILE"+struct.pack("<i256s", len(data),\
                    str(self.fileNames[fileindex])))
                for x in xrange(0, (len(data)+1023)/1024):
                    clientSocket.sendall(data[x*1024:(x+1)*1024])
                    time.sleep(0.05)
            clientSocket.sendall('FEND')
            clientSocket.close()
        except socket.error, msg:
            logging.error('Sending files failed. %s', str(msg))


class FileReceiverThread(threading.Thread):
    def __init__(self, receive_port):
        threading.Thread.__init__(self)
        self.fileDone = 0
        self.fileSize = 1
        self.receive_port = receive_port


    def run(self):
        try:
            logging.debug('Listening for response on port %s', self.receive_port)
            localSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            localSocket.settimeout(60.0)
            localSocket.bind(('', self.receive_port))
            localSocket.listen(1)
            con, addr = localSocket.accept()
            logging.debug('Connection address: %s', addr)
            con.settimeout(60.0)
            while True:
                data = getAllBytes(con, 4)
                if not data:
                    break
                elif data == 'FEND':
                    break
                elif data == 'FILE':
                    data = getAllBytes(con, 260)
                    self.fileSize, fileName = struct.unpack("<i256s", data)
                    fileName = fileName.replace('\0', '')
                    logging.debug("%s %s", self.fileSize, fileName)
                    fileName = str(fileName)
                    logging.debug('fileName %s', fileName)
                    f = open('../roms/' + fileName, 'wb')
                    fileLeft = self.fileSize
                    while fileLeft:
                        data = con.recv(min(fileLeft, 1024))
                        fileLeft = max(0, fileLeft - len(data))
                        self.fileDone = self.fileSize - fileLeft
                        logging.debug('percent done %s', self.fileDone * 100 / self.fileSize)
                        f.write(data)
                    f.close()
                    logging.debug('file finished')
                else:
                    raise Exception('ERROR GETTING FILES (NO FILE OR FEND)')
            logging.debug('Finished getting all files!')
            del localSocket
        except socket.error as msg:
            logging.error("Transfer Failed: %s", str(msg))
