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

# general pin input/output for motion detector device
import time

import Adafruit_BBIO.GPIO as GPIO

GPIO.setup('P9_15', GPIO.IN)

file_handle = open('movement_log.txt', 'w')

while True:
    GPIO.wait_for_edge("P9_15", GPIO.RISING)
    log_start = time.strftime("%a, %d %b %Y %H:%M:%S")
    GPIO.wait_for_edge("P9_15", GPIO.FALLING)
    log_end = time.strftime("%a, %d %b %Y %H:%M:%S")
    file_handle.write("+" + "-" * 40 + "\n")
    file_handle.write("| Start: %s\n" % log_start)
    file_handle.write("| End: %s\n" % log_end)
