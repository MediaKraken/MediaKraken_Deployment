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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import os
import rtsimple as rt


class CommonMetadataRottenTomatoes(object):
    """
    Class for interfacing with rotten tomatoes
    """
    def __init__(self):
        import ConfigParser
        config_handle = ConfigParser.ConfigParser()
        config_handle.read("MediaKraken.ini")
        rt.API_KEY = config_handle.get('API', 'RottenTomatoes').strip()


    def com_rt_search(movie_title, movie_year=None):
        """
        # search for movie title and year
        """
        movie = rt.Movies()
        response = movie.search(q=movie_title)
        for m in movie.movies:
            logging.info("rt: %s %s %s", m['title'], m['id'], m['alternate_ids'])
        return movie
