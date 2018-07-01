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

# https://github.com/MediaKraken-Dependancies/pyowm
import pyowm


class CommonNetOWM(object):
    def __init__(self, api_key):
        self.owm_inst = pyowm.OWM(api_key)

    def com_net_owm_get_weather(self, city_location, country_location):
        self.observation = self.owm_inst.weather_at_place('%s,%s',
                                                          (city_location, country_location))
        w = self.observation.get_weather()
        w.get_wind()  # {'speed': 4.6, 'deg': 330}
        w.get_humidity()  # 87
        w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

    def com_net_own_get_weather_local(self, x_cord, y_cord):
        self.observation_list = self.owm_inst.weather_around_coords(x_cord, y_cord)
