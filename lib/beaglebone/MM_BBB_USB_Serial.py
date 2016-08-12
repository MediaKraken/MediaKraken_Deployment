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
Arduino_Board_NeoPixel = Arduino('9600', port="/dev/ttyACM0")   # Neo1
Arduino_Board_Stepper = Arduino('9600', port="/dev/ttyACM1")    # Stp1

# Arduino Mega 2560
Arduino_Board_LCD_Center = Arduino('9600', port="/dev/ttyACM2")

def octmote_arduino_usb_serial_digitalwrite(board_type, pin_number, pin_high_low):
    pass

def octmote_arduino_usb_serial_writestring(board_type, serial_string):
    if board_type == "Neo1":
        Arduino_Board_NeoPixel.SoftwareSerial.write(serial_string)
    else:
        Arduino_Board_Stepper.SoftwareSerial.write(serial_string)

def octmote_arduino_usb_serial_receivestring():
    pass

#while True:
#    Arduino_Board_NeoPixel.SoftwareSerial.write("test") #Send some data
#    time.sleep(1)
#    Arduino_Board_NeoPixel.digitalWrite(13, "HIGH")
#    time.sleep(1)
#    Arduino_Board_NeoPixel.digitalWrite(13, "LOW") #Set digital pin 13 voltage
#    time.sleep(1)
