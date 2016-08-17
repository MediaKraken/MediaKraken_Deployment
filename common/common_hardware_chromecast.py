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

# supported formats list
# https://developers.google.com/cast/docs/media#subtitles--closed-captions

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import pychromecast
import pychromecast.controllers.youtube as youtube
from pychromecast.controllers import BaseController


class CommonHardwareChromecast(object):
    """
    Class for interfacing with chromecast
    """
    def __init__(self):
        self.chromecast_dict = None


    def com_chromecast_discover_dict(self):
        """
        # find chromecast as dict
        """
        self.chromecast_dict = pychromecast.get_chromecasts_as_dict().keys()
        return self.chromecast_dict


    def com_chromecast_info(self):
        """
        # get detail by name
        """
        return self.cast.device


    def com_chromecast_status(self):
        """
        # get status by name
        """
        return self.cast.status


    def com_chromecast_connect_by_name(self, key_name):
        """
        # connect to device
        """
        self.cast = pychromecast.get_chromecast(friendly_name=key_name)
        # Wait for cast device to be ready
        self.cast.wait()
        self.chromecast_device = self.cast.media_controller


    def com_chromecast_play_yt(self, yt_id):
        """
        # play youtube video
        """
        yt_controller = YouTubeController()
        self.chromecast_device.register_handler(yt_controller)
        yt_controller.play_video(yt_id)


    def com_chromecast_play_media(self, media_file, media_type):
        """
        # play media file
        """
        self.chromecast_device.play_media(media_file, media_type)


    def com_chromecast_device_command(self, command):
        """
        # send chromecast commands
        """
        if command == "Pause":
            self.chromecast_device.pause()
        elif command == "Play":
            self.chromecast_device.play()
        elif command == "Stop":
            self.chromecast_device.stop()


    def com_chromecast_device_close(self):
        """
        Close the chromecast device
        """
        self.chromecast_device.quit_app()
