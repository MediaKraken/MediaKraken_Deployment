'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import requests


class common_backup_crashplan_api:
    """
    Class for interfacing with crashplan
    """
    def __init__(self, user_name, user_password):
        crash_resp = requests.get('https://master-server.example.com:4285/api/Computer',\
                auth=(user_name, user_password))
        logging.debug("resp: %s", crash_resp.status_code)
        logging.debug("text: %s", crash_resp.text)
