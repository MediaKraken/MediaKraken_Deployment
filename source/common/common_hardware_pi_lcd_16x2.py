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

import time

import lcddriver


# https://github.com/MediaKraken-Dependancies/lcd

class CommonHardwarePILCD16x2:
    """
    Class for interfacing with pi lcd 16x2
    """

    def __init__(self):
        self.display = lcddriver.lcd()

    def com_hard_pi_lcd_text(self):
        # Remember that your sentences can only be 16 characters long!
        print("Writing to display")
        self.display.lcd_display_string("Greetings Human!",
                                        1)  # Write line of text to first line of display
        self.display.lcd_display_string("Demo Pi Guy code",
                                        2)  # Write line of text to second line of display
        time.sleep(2)  # Give time for the message to be read
        self.display.lcd_display_string("I am a display!",
                                        1)  # Refresh the first line of display with a different message
        time.sleep(2)  # Give time for the message to be read
        self.display.lcd_clear()  # Clear the display of any data
        time.sleep(2)

    def com_hard_pi_lcd_longtext(self):
        def long_string(display, text='', num_line=1, num_cols=20):
            """
            Parameters: (driver, string to print, number of line to print, number of columns of your display)
            Return: This function send to display your scrolling string.
            """
            if (len(text) > num_cols):
                display.lcd_display_string(text[:num_cols], num_line)
                time.sleep(1)
                for i in range(len(text) - num_cols + 1):
                    text_to_print = text[i:i + num_cols]
                    display.lcd_display_string(text_to_print, num_line)
                    time.sleep(0.2)
                time.sleep(1)
            else:
                display.lcd_display_string(text, num_line)

            # Example of short string

        long_string(self.display, "Hello World!", 1)
        time.sleep(1)

        # Example of long string
        long_string(self.display, "Hello again. This is a long text.", 2)
        self.display.lcd_clear()
        time.sleep(1)

        while True:
            # An example of infinite scrolling text
            long_string(self.display, "Hello friend! This is a long text!", 2)
