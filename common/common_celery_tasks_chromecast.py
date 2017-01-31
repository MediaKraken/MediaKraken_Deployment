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
sys.path.append('.')
sys.path.append('..')
from network import network_base_string as network_base


@common_celery.app.task(queue='mkque')
def com_celery_chrome_play(media_json):
    """
    play media file to chromecast
    """
    logging.info('task: play')
    network_base.NetworkEvents.broadcast_message(media_json)


@common_celery.app.task(queue='mkque')
def com_celery_chrome_stop(media_json):
    """
    stop media file to chromecast
    """
    logging.info('task: stop')
    pass


@common_celery.app.task(queue='mkque')
def com_celery_chrome_pause(media_json):
    """
    pause media file to chromecast
    """
    logging.info('task: pause')
    pass


@common_celery.app.task(queue='mkque')
def com_celery_chrome_mute(media_json):
    """
    mute audio chromecast
    """
    logging.info('task: mute')
    pass


@common_celery.app.task(queue='mkque')
def com_celery_chrome_vol_up(media_json):
    """
    chromecast volume up
    """
    logging.info('task: vol up')
    pass


@common_celery.app.task(queue='mkque')
def com_celery_chrome_vol_down(media_json):
    """
    chromecast volume down
    """
    logging.info('task: vol down')
    pass


@common_celery.app.task(queue='mkque')
def com_celery_chrome_vol_set(media_json):
    """
    chromecast volume set
    """
    logging.info('task: vol set')
    pass


@common_celery.app.task(queue='mkque')
def com_celery_chrome_status(chrome_json):
    """
    chromecast status
    """
    logging.info('task: status')
    pass
