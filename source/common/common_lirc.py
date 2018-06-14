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

import pylirc as lirc


class CommonLIRC(object):
    """
    Class for interfacing with lirc
    """

    def __init__(self, option_config_json):
        pass

    def com_lirc_init(self, app_string="./conf"):
        """
        Initialize LIRC
        """
        return lirc.init("MediaKraken", app_string, False)

    def com_lirc_load_config(self, config_file):
        """
        Load config file for LIRC
        """
        lirc.load_config_file(config_file)

    def com_lirc_nextcode(self):
        """
        grab returend code
        """
        return lirc.nextcode()

    def com_lirc_close(self):
        """
        Shutdown LIRC
        """
        lirc.exit()
