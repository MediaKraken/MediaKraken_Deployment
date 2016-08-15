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
#import logging
import pychromecast
import pychromecast.controllers.youtube as youtube
from pychromecast.controllers import BaseController


class CommonHardwareChromecast(object):
    """
    Class for interfacing with chromecast
    """
    def __init__(self):
        self.chromecast_dict = None


    def MK_Chromecast_Discover_Dict(self):
        """
        # find chromecast as dict
        """
        self.chromecast_dict = pychromecast.get_chromecasts_as_dict().keys()
        return self.chromecast_dict


    def MK_Chromecast_Info(self):
        """
        # get detail by name
        """
        return self.cast.device


    def MK_Chromecast_Status(self):
        """
        # get status by name
        """
        return self.cast.status


    def MK_Chromecast_Connect_by_Name(self, key_name):
        """
        # connect to device
        """
        self.cast = pychromecast.get_chromecast(friendly_name=key_name)
        # Wait for cast device to be ready
        self.cast.wait()
        self.chromecast_device = self.cast.media_controller


    def MK_Chromecast_Play_YT(self, yt_id):
        """
        # play youtube video
        """
        yt_controller = YouTubeController()
        self.chromecast_device.register_handler(yt_controller)
        yt_controller.play_video(yt_id)


    def MK_Chromecast_Play_Media(self, media_file, media_type):
        """
        # play media file
        """
        self.chromecast_device.play_media(media_file, media_type)


    def MK_Chromecast_Device_Command(self, command):
        """
        # send chromecast commands
        """
        if command == "Pause":
            self.chromecast_device.pause()
        elif command == "Play":
            self.chromecast_device.play()
        elif command == "Stop":
            self.chromecast_device.stop()


    def MK_Chromecast_Device_Close(self):
        """
        Close the chromecast device
        """
        self.chromecast_device.quit_app()
