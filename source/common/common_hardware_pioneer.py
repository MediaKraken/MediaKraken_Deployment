"""
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
"""

import socket

from common import common_logging_elasticsearch_httpx

from . import common_global


class CommonHardwarePioneer:
    """
    Class for interfacing with pioneer equipment over network connection
    """

    def __init__(self, device_ip, device_port):
        self.pioneer_inst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pioneer_inst.connect((device_ip, device_port))
        self.pioneer_inst.settimeout(1)

    def com_hardware_command(self, command):
        buf = bytes(command + "\r\n", 'ascii')
        self.pioneer_inst.send(buf)
        datastr = []
        data = bytearray()
        try:
            msg = self.pioneer_inst.recv(4096)
        except socket.error as e:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='error', message_text={'Pioneer socket error': e})
        else:
            if len(msg) == 0:
                common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                     message_text={
                                                                         'pioneer shutdown on server end'})
            else:
                common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                     message_text={
                                                                         'pioneer data': msg})
                while 1:
                    rxbuf = self.pioneer_inst.recv(1024)
                    if rxbuf:
                        data.extend(rxbuf)
                        datastr.append(data.decode(encoding='ascii'))
                        break
                    else:
                        self.pioneer_inst.shutdown(socket.SHUT_WR)
                        self.pioneer_inst.close()
                        break
                return data.decode(encoding='ascii')

    def com_hardware_close(self):
        self.pioneer_inst.shutdown(socket.SHUT_WR)
        self.pioneer_inst.close()


"""
Volume:
    VD = VOLUME DOWN
    MZ = MUTE ON/OFF
    VU = VOLUME UP
    ?V = QUERY VOLUME
Power control:
    PF = POWER OFF
    PO = POWER ON
    ?P = QUERY POWER STATUS
Input selection
    05FN = TV/SAT
    01FN = CD
    03FN = CD-R/TAPE
    04FN = DVD
    19FN = HDMI1
    05FN = TV/SAT
    00FN = PHONO
    03FN = CD-R/TAPE
    26FN = HOME MEDIA GALLERY(Internet Radio)
    15FN = DVR/BDR
    05FN = TV/SAT
    10FN = VIDEO 1(VIDEO)
    14FN = VIDEO 2
    19FN = HDMI1
    20FN = HDMI2
    21FN = HDMI3
    22FN = HDMI4
    23FN = HDMI5
    24FN = HDMI6
    25FN = BD
    17FN = iPod/USB
    FU = INPUT CHANGE (cyclic)
    ?F = QUERY INPUT
"""
