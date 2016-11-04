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

# send serial command to arduino via USB
from Arduino import Arduino

# Arduino UNO R3
ARDUINO_BOARD_NEOPIXEL = Arduino('9600', port="/dev/ttyACM0")   # Neo1
ARDUINO_BOARD_STEPPER = Arduino('9600', port="/dev/ttyACM1")    # Stp1
# Arduino Mega 2560
ARDUINO_BOARD_LCD_CENTER = Arduino('9600', port="/dev/ttyACM2")


def com_arduino_usb_serial_digitalwrite(board_type, pin_number, pin_high_low):
    pass


def com_arduino_usb_serial_writestring(board_type, serial_string):
    if board_type == "Neo1":
        ARDUINO_BOARD_NEOPIXEL.SoftwareSerial.write(serial_string)
    else:
        ARDUINO_BOARD_STEPPER.SoftwareSerial.write(serial_string)


def com_arduino_usb_serial_receivestring():
    pass


#while True:
#    ARDUINO_BOARD_NEOPIXEL.SoftwareSerial.write("test") #Send some data
#    time.sleep(1)
#    ARDUINO_BOARD_NEOPIXEL.digitalWrite(13, "HIGH")
#    time.sleep(1)
#    ARDUINO_BOARD_NEOPIXEL.digitalWrite(13, "LOW") #Set digital pin 13 voltage
#    time.sleep(1)
