"""
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
"""

import flickrapi


class CommonNetworkFlickr:
    """
    Class for interfacing with Flickr
    """

    def __init__(self, api_key, api_secret):
        self.flickr = flickrapi.FlickrAPI(
            api_key, api_secret, format='parsed-json')

#        photos = flickr.photos.search(user_id='73509078@N00', per_page='10')
#        sets = flickr.photosets.getList(user_id='73509078@N00')
