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

# https://github.com/MediaKraken-Dependancies/pyinsane
import pyinsane2
from common import common_file


class CommonHardwareScanner:
    def __init__(self):
        pyinsane2.init()

    def com_hardware_scanner_close(self):
        pyinsane2.exit()

    def com_hardware_scanner_find(self):
        return pyinsane2.get_devices()

    def com_hardware_scanner_scan(self, scanner_device, resolution, file_name):
        try:
            pyinsane2.set_scanner_opt(
                scanner_device, 'resolution', [resolution])
            pyinsane2.set_scanner_opt(scanner_device, 'mode', ['Color'])
            pyinsane2.maximize_scan_area(scanner_device)
            scan_session = scanner_device.scan(multiple=False)
            try:
                while True:
                    scan_session.scan.read()
            except EOFError:
                pass
            image = scan_session.images[-1]
            common_file.com_file_save_data(file_name, image)
        finally:
            pyinsane2.exit()
