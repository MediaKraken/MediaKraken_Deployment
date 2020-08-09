"""
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
"""

# https://github.com/MediaKraken-Dep/tripplite
from tripplite import Battery

'''
{
    "config": {
        "frequency": 60,  # Hz
        "power": 1500,  # VA
        "voltage": 120  # V
    },
    "health": 100,  # %
    "input": {
        "frequency": 59.7,  # Hz
        "voltage": 117.2  # V
    },
    "output": {
        "power": 324,  # W
        "voltage": 117.2  # V
    },
    "status": {
        "ac present": true,
        "below remaining capacity": true,
        "charging": false,
        "discharging": false,
        "fully charged": true,
        "fully discharged": false,
        "needs replacement": false,
        "shutdown imminent": false
    },
    "time to empty": 1004  # s
}'''


def com_hard_tripplite():
    with Battery() as battery:
        return battery.get()
