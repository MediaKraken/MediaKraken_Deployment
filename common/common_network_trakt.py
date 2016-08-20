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
import trakt
from trakt.calendar import PremiereCalendar
from trakt import movies
from trakt.movies import dismiss_recommendation
from trakt.movies import get_recommended_movies
from trakt.movies import Movie, rate_movies
from trakt.people import Person
from trakt.tv import TVShow
from trakt.users import User


class CommonNetworkTrakt(object):
    """
    Class for interfacing with Trakt
    """
    def __init__(self, response, option_config_json):
        # setup login/user info
        trakt.configuration.defaults.client(id=option_config_json['Trakt']['ClientID'],
            secret=option_config_json['Trakt']['SecretKey']
        )


    def com_net_trakt_calendar_by_days(self, day_count):
        """
        # calendar by days
        """
        return PremiereCalendar(days=day_count)


    def com_net_trakt_dismiss_recommendation(self, imdb_id, imdb_title, imdb_year):
        """
        # dismiss recommendation
        """
        #dismiss_recommendation(imdb_id='tt3139072', title='Son of Batman', year=2014)
        dismiss_recommendation(imdb_id=imdb_id, title=imdb_title, year=imdb_year)
