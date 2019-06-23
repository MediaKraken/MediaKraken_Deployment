'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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

from pylgtv import WebOsClient


class CommonNetworkWebOS:
    """
    Class for interfacing with webos
    """

    def __init__(self, host_name):
        self.webos_inst = WebOsClient(host_name)

    def com_net_webos_app_list(self):
        return self.webos_inst.webos_client.get_apps()

    def com_net_webos_app_launch(self, app_name):
        self.webos_inst.webos_client.launch_app(app_name)

    def com_net_webos_get_current_app(self):
        self.webos_inst.webos_client.get_current_app()

    def com_net_webos_close_app(self, app_name):
        self.webos_inst.webos_client.close_app(app_name)

    def com_net_webos_get_services(self):
        self.webos_inst.webos_client.get_services()

    def com_net_webos_power_off(self):
        self.webos_inst.webos_client.power_off()

    def com_net_webos_power_on(self):
        self.webos_inst.webos_client.power_on()

    def com_net_webos_turn_3d_on(self):
        self.webos_inst.webos_client.turn_3d_on()

    def com_net_webos_turn_3d_off(self):
        self.webos_inst.webos_client.turn_3d_off()

    def com_net_webos_get_inputs(self):
        self.webos_inst.webos_client.get_inputs()

    def com_net_webos_get_input(self):
        self.webos_inst.webos_client.get_input()

    def com_net_webos_set_input(self, input):
        self.webos_inst.webos_client.set_input(input)

    def com_net_webos_get_audio_status(self):
        self.webos_inst.webos_client.get_audio_status()

    def com_net_webos_get_muted(self):
        self.webos_inst.webos_client.get_muted()

    def com_net_webos_set_mute(self, mute):
        self.webos_inst.webos_client.set_mute(mute)

    def com_net_webos_get_volume(self):
        self.webos_inst.webos_client.get_volume()

    def com_net_webos_set_volume(self, volume):
        self.webos_inst.webos_client.set_volume(volume)

    def com_net_webos_volume_up(self):
        self.webos_inst.webos_client.volume_up()

    def com_net_webos_volume_down(self):
        self.webos_inst.webos_client.volume_down()

    def com_net_webos_channel_up(self):
        self.webos_inst.webos_client.channel_up()

    def com_net_webos_channel_down(self):
        self.webos_inst.webos_client.channel_down()

    def com_net_webos_get_channels(self):
        self.webos_inst.webos_client.get_channels()

    def com_net_webos_get_current_channel(self):
        self.webos_inst.webos_client.get_current_channel()

    def com_net_webos_get_channel_info(self):
        self.webos_inst.webos_client.get_channel_info()

    def com_net_webos_set_channel(self, channel):
        self.webos_inst.webos_client.set_channel(channel)

    def com_net_webos_play(self):
        self.webos_inst.webos_client.play()

    def com_net_webos_pause(self):
        self.webos_inst.webos_client.pause()

    def com_net_webos_stop(self):
        self.webos_inst.webos_client.stop()

    def com_net_webos_close(self):
        self.webos_inst.webos_client.close()

    def com_net_webos_rewind(self):
        self.webos_inst.webos_client.rewind()

    def com_net_webos_fast_forward(self):
        self.webos_inst.webos_client.fast_forward()

    def com_net_webos_send_enter_key(self):
        self.webos_inst.webos_client.send_enter_key()

    def com_net_webos_send_delete_key(self):
        self.webos_inst.webos_client.send_delete_key()

    def com_net_webos_open_url(self, url):
        self.webos_inst.webos_client.open_url(url)

    def com_net_webos_close_web(self):
        self.webos_inst.webos_client.close_web()
