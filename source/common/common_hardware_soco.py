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

# https://github.com/MediaKraken-Dependancies/SoCo
import soco
from soco import SoCo


def com_hardware_soco_discover():
    return soco.discover()


# def com_hardware_soco_mute(self, zone, mute_status):
#        zone_list[zone].mute = mute_status

class CommonHardwareSoco(object):
    """
    Class for Sonos
    """

    def __init__(self, ip_addr):
        self.soco_inst = SoCo(ip_addr)

    def com_hardware_soco_name(self):
        return self.soco_inst.player_name

    def com_hardware_soco_volume(self, set_volume):
        self.soco_inst.volume = set_volume

    def com_hardware_soco_light_status(self, light_status):
        self.soco_inst.status_light = light_status

    def com_hardware_soco_play_url(self, url):
        self.soco_inst.play_uri(url)

    def com_hardware_soco_pause(self):
        self.soco_inst.pause()

    def com_hardware_soco_play(self):
        # Play a stopped or paused track
        self.soco_inst.play()
