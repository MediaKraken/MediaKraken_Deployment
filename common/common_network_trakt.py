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
import logging
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import trakt
from trakt.calendar import PremiereCalendar
from trakt import movies
from trakt.movies import dismiss_recommendation
from trakt.movies import get_recommended_movies
from trakt.movies import Movie, rate_movies
from trakt.people import Person
from trakt.tv import TVShow
from trakt.users import User


class MK_Common_Trakt_API:
    """
    Class for interfacing with Trakt
    """
    def __init__(self, response):
        # setup login/user info
        trakt.configuration.defaults.client(
            id=Config.get('Trakt', 'ClientID').strip(),
            secret=Config.get('Trakt', 'SecretKey').strip()
        )


    # calendar by days
    def MK_Common_Trakt_Calendar_By_Days(day_count):
        return PremiereCalendar(days=day_count)


    # dismiss recommendation
    def MK_Common_Trakt_Dismiss_Recommendation(imdb_id, imdb_title, imdb_year):
        dismiss_recommendation(imdb_id='tt3139072', title='Son of Batman', year=2014)
