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

import sys

from beautifulhue.api import Bridge


class CommonHardwareBeatifulHue:
    """
    Class for interfacing with beatifulhue
    """

    def __init__(self, ip_addr, user_id):
        self.beatifulhue_inst = Bridge(
            device={'ip': ip_addr}, user={'name': user_id})

    def com_hardware_beatifulhue_config(self):
        created = False
        print('Press the button on the Hue bridge')
        while not created:
            resource = {'user': {'devicetype': 'MediaKraken',
                                 'name': '5kPvIJGlzmWgB2mNDxb-ILEKZGAiBILcpt862U9m'}}
            response = self.beatifulhue_inst.config.create(resource)['resource']
            if 'error' in response[0]:
                if response[0]['error']['type'] != 101:
                    print('Unhandled error creating configuration on the Hue')
                    sys.exit(response)
            else:
                created = True

    def com_hardware_beatifulhue_info(self):
        return self.beatifulhue_inst.config.get({'which': 'system'})['resource']

    def com_hardware_beatifulhue_get_light(self, light_id):
        # n
        # 'new'
        # 'all'
        return self.beatifulhue_inst.light.get({'which': light_id, 'verbose': True})

    def com_hardward_beatifulhue_update_light(self, light_id, attr_name, attr_desc):
        resource = {
            'which': light_id,
            'data': {
                'attr': {attr_name: attr_desc}
            }
        }
        self.beatifulhue_inst.light.update(resource)


stuff = CommonHardwareBeatifulHue(
    '10.0.0.225', '5kPvIJGlzmWgB2mNDxb-ILEKZGAiBILcpt862U9m')
# stuff.com_hardware_beatifulhue_config()
print((stuff.com_hardware_beatifulhue_info()))
print((stuff.com_hardware_beatifulhue_get_light('all')))
