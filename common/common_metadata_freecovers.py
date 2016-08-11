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


'''
Apparenlty their API was disabled a year ago due to abuse
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import urllib2
import urllib
from xml.dom.minidom import parse
import MK_Common_Network

'''
Anime DVD
Blu-Ray Movie
DVD Movie
HD-DVD Movie
GameCube
Music CD
Music DVD
Other
Other Console
PC Apps
PC Games
Playstation
Playstation 2
Playstation 3
PSP
Soundtrack
TV Series
VCD
VHS
Wii
Xbox
Xbox 360
'''

# general freecovers search
def MK_Common_FreeCovers_Search(search_string, search_categories):
    #xml_data = parse(MK_Common_Network.MK_Network_Fetch_From_URL('http://www.freecovers.net/api/search/' + search_string, None))
    #for node in xml_data.getElementsByTagName('name'):
    request = urllib2.Request('http://www.freecovers.net/api/search/', urllib.urlencode({'search': search_string}))
    handler = urllib2.urlopen(request)
    print(handler.read())


MK_Common_FreeCovers_Search('Megadeath', None):
    pass
