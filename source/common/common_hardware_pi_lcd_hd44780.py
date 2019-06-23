'''
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
'''

import pigpio
from RPLCD.gpio import CharLCD as CharLCDGPIO
from RPLCD.i2c import CharLCD as CharLCDI2C
from RPLCD.pigpio import CharLCD as CharLCDPIGPIO
from RPi import GPIO


# https://github.com/MediaKraken-Dependancies/RPLCD

class CommonHardwarePIHD44780I2C:
    """
    Class for interfacing with pi lcd HD44780
    """

    def __init__(self):
        self.lcd_inst = CharLCDI2C(i2c_expander='PCF8574', address=0x27, port=1,
                                   cols=20, rows=4, dotsize=8,
                                   charmap='A02',
                                   auto_linebreaks=True,
                                   backlight_enabled=True)

    def com_hard_pi_hd44780_write(self, lcd_string, x_pos=None, y_pos=None):
        if x_pos is not None:
            self.lcd_inst.cursor_pos = (x_pos, y_pos)
        self.lcd_inst.write_string(lcd_string)

    def com_hard_pi_hd44780_clear(self):
        self.lcd_inst.clear()

    def com_hard_pi_hd44780_close(self, clear_screen=True):
        self.lcd_inst.close(clear=clear_screen)


class CommonHardwarePIHD44780GPIO:
    """
    Class for interfacing with pi lcd HD44780
    """

    def __init__(self):
        self.lcd_inst = CharLCDGPIO(pin_rs=15, pin_rw=18, pin_e=16,
                                    pins_data=[21, 22, 23, 24],
                                    numbering_mode=GPIO.BOARD,
                                    cols=20, rows=4, dotsize=8,
                                    charmap='A02',
                                    auto_linebreaks=True)

    def com_hard_pi_hd44780_write(self, lcd_string, x_pos=None, y_pos=None):
        if x_pos is not None:
            self.lcd_inst.cursor_pos = (x_pos, y_pos)
        self.lcd_inst.write_string(lcd_string)

    def com_hard_pi_hd44780_clear(self):
        self.lcd_inst.clear()

    def com_hard_pi_hd44780_close(self, clear_screen=True):
        self.lcd_inst.close(clear=clear_screen)


class CommonHardwarePIHD44780POGPIO:
    """
    Class for interfacing with pi lcd HD44780
    """

    def __init__(self):
        pi = pigpio.pi()
        self.lcd_inst = CharLCDPIGPIO(pi,
                                      pin_rs=15, pin_rw=18, pin_e=16,
                                      pins_data=[21, 22, 23, 24],
                                      cols=20, rows=4, dotsize=8,
                                      charmap='A02',
                                      auto_linebreaks=True)

    def com_hard_pi_hd44780_write(self, lcd_string, x_pos=None, y_pos=None):
        if x_pos is not None:
            self.lcd_inst.cursor_pos = (x_pos, y_pos)
        self.lcd_inst.write_string(lcd_string)

    def com_hard_pi_hd44780_clear(self):
        self.lcd_inst.clear()

    def com_hard_pi_hd44780_close(self, clear_screen=True):
        self.lcd_inst.close(clear=clear_screen)
