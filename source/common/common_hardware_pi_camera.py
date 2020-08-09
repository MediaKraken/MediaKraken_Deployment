"""
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

import os

import time
# https://github.com/MediaKraken-Dependancies/picamera
from picamera import PiCamera


class CommonHardwarePICamera:
    """
    Class for interfacing with pi camera
    """

    def __init__(self, rez_width=1024, rez_height=768):
        self.camera = PiCamera()
        self.camera.resolution = (rez_width, rez_height)
        self.camera.start_preview()
        # Camera warm-up time
        time.sleep(2)

    def com_hardware_pi_camera_image(self, file_name):
        self.camera.capture(file_name)

    def com_hardware_pi_camera_stream(self, file_name):
        self.my_file = open(file_name, 'wb')
        self.camera.capture(self.my_file, 'png')

    def com_hardware_pi_camera_stream_stop(self):
        self.my_file.close()

    def com_hardware_pi_camera_timelapse(self, seconds, file_save_path):
        for filename in self.camera.capture_continuous('img{counter:03d}.jpg'):
            self.com_hardware_pi_camera_image(os.path.join(file_save_path, filename))
            time.sleep(seconds)

    def com_hardware_pi_camera_led(self, led_status=False):
        self.camera.led = led_status

# TODO provide network stream 3.9
# TODO record video file by time 3.10
# TODO motion detect record 3.12
# TODO 3.13 Recording to a network stream
# TODO 3.15 Overlaying text on the output
# TODO 4.10. Web streaming
