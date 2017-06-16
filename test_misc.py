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

from __future__ import absolute_import, division, print_function, unicode_literals
from common import common_network_mediakraken

# print how the server output works
#print(common_network_mediakraken.com_net_mediakraken_find_server())

stuff = {}

stuff['a'] = ('bah', 'bah2')


print(stuff)


stuff2 = 'jo32ljf02fj2ofjofjfofjfo'

print(stuff2[-3:])



import json

json_data = json.dumps({
  "result":[
    {
      "run":[
        {
          "action":"stop"
        },
          {
              "action": "start"
          },
          {
              "action": "start"
          }
      ],
      "find": "true"
    }
  ]
})

item_dict = json.loads(json_data)
print(len(item_dict['result'][0]['run']))
