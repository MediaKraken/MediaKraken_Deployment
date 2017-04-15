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
import logging # pylint: disable=W0611
from . import common_celery
import sys
#sys.path.append("/mediakraken")
sys.path.append('.')
from network import network_base_string as network_base


@common_celery.app.task(queue='mkque')
def com_celery_chrome_task(media_json):
    """
    celery task for chromecast
    """
    logging.info('chrome task: %s', media_json)
    network_base.NetworkEvents.broadcast_celery_message(media_json)
