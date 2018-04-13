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

#
# they decided to go pay only
#

# from __future__ import absolute_import, division, print_function, unicode_literals
# import logging # pylint: disable=W0611
# import rtsimple as rt
#
#
# class CommonMetadataRottenTomatoes(object):
#    """
#    Class for interfacing with rotten tomatoes
#    """
#    def __init__(self, option_config_json):
#        rt.API_KEY = option_config_json['API']['RottenTomatoes']
#
#
#    def com_rt_search(self, movie_title, movie_year=None):
#        """
#        # search for movie title and year
#        """
#        movie = rt.Movies()
#        response = movie.search(q=movie_title)
#        for movie_data in movie.movies:
#            common_global.es_inst.com_elastic_index('info', {'stuff':"rt: %s %s %s", movie_data['title'], movie_data['id'],
#                movie_data['alternate_ids'])
#        return movie
