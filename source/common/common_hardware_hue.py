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

from phue import Bridge


class CommonHardwareHue:
    """
    Class for interfacing with hue
    """

    def __init__(self, ip_addr):
        self.hue_inst = Bridge(ip_addr, config_file_path='/mediakraken/phue/phue.config')
        # If the app is not registered and the button is not pressed,
        # press the button and call connect() (this only needs to be run a single time)
        self.hue_inst.connect()

    def com_hardware_hue_get_api(self):
        # Get the bridge state (This returns the full dictionary that you can explore)
        return self.hue_inst.get_api()

    def com_hardware_hue_get_lights(self):
        return self.com_hardware_hue_get_api()['lights']

    def com_hardware_hue_light_info(self, light_num, status_type):
        # 'on' - wether on/off
        # 'name' - name of light
        return self.hue_inst.get_light(light_num, status_type)

    def com_hardware_hue_light_set(self, light_list, function_type='on', var_value=True):
        # You can also control multiple lamps by sending a list as lamp_id
        # 'on' on/off via bool
        # 'bri' 1-100 value for brightness
        self.hue_inst.set_light(light_list, function_type, var_value)

# test = CommonHardwareHue('10.0.0.225')
# print(test.com_hardware_hue_get_api())
# # print(test.com_hardware_hue_get_lights())
# # print(test.com_hardware_hue_light_onoff(1))
# print(test.com_hardware_hue_light_set((1, 2, 3), 'on', False))
# print(test.com_hardware_hue_light_set((1, 2, 3), 'bri', 10))
# print(test.com_hardware_hue_light_name(1))

# # You can also use light names instead of the id
# b.get_light('Kitchen')
# b.set_light('Kitchen', 'bri', 254)
#
# # Also works with lists
# b.set_light(['Bathroom', 'Garage'], 'on', False)
#
# # The set_light method can also take a dictionary as the second argument to do more fancy stuff
# # This will turn light 1 on with a transition time of 30 seconds
# command =  {'transitiontime' : 300, 'on' : True, 'bri' : 254}
# b.set_light(1, command)
