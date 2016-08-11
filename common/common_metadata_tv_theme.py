'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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

import logging
from bs4 import BeautifulSoup
import MK_Common_Network
import MK_Common_String


# try to grab theme from tvtunes
def MK_Common_TVTheme_Download(media_name):
    data = BeautifulSoup(MK_Common_Network.MK_Network_Fetch_From_URL("http://www.televisiontunes.com/" + MK_Common_String.MK_Common_String_Title(media_name).replace(' ','_') + ".html", None)).find(id="download_song")
    if data is not None:
        logging.debug('href: %s', data['href'])
        MK_Common_Network.MK_Network_Fetch_From_URL("http://www.televisiontunes.com" + data['href'], 'theme.mp3')


# MK_Common_TVTheme_Download("V")