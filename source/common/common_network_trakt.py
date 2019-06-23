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

import trakt
import trakt.core
from trakt import movies
from trakt.users import User
from trakt.calendar import PremiereCalendar
from trakt.movies import (Movie, dismiss_recommendation, get_recommended_movies)
from trakt.people import Person
from trakt.tv import TVShow


class CommonNetworkTrakt:
    """
    Class for interfacing with Trakt
    """

    def __init__(self, option_config_json):
        # setup login/user info
        trakt.core.OAUTH_TOKEN = option_config_json['Trakt']['ApiKey']  # the oauth key
        trakt.core.CLIENT_ID = option_config_json['Trakt']['ClientID']
        trakt.core.CLIENT_SECRET = option_config_json['Trakt']['SecretKey']

    def com_net_trakt_calendar_by_days(self, day_count=1):
        """
        # calendar by days
        """
        return PremiereCalendar(days=day_count)

    def com_net_trakt_dismiss_recommendation(self, imdb_id, imdb_title, imdb_year):
        """
        # dismiss recommendation
        """
        # dismiss_recommendation(imdb_id='tt3139072', title='Son of Batman', year=2014)
        dismiss_recommendation(imdb_id=imdb_id, title=imdb_title, year=imdb_year)

    def com_net_trakt_get_recommended(self):
        return get_recommended_movies()

    def com_net_trakt_get_genre(self):
        return movies.genres()

    def com_net_trakt_get_trending(self):
        return movies.trending_movies()

    def com_net_trakt_get_updated(self):
        return movies.updated_movies()

    def com_net_trakt_set_seen_movie(self, movie_name_year):
        """
        Set seen status on media
        """
        media_instance = Movie(movie_name_year)
        media_instance.mark_as_seen()

    def com_net_trakt_add_movie(self, movie_name_year):
        """
        Set add media
        """
        media_instance = Movie(movie_name_year)
        media_instance.add_to_library()

    def com_net_trakt_set_watching_movie(self, movie_name_year):
        """
        Set watching status on media
        """
        media_instance = Movie(movie_name_year)
        media_instance.watching_now()

    def com_net_trakt_set_rating_movie(self, movie_name_year, media_rating):
        """
        Set user rating on media
        """
        media_instance = Movie(movie_name_year)
        media_instance.rate(media_rating)

    def com_net_trakt_get_person(self, person_name, search=False):
        if search:
            return Person(person_name)
        else:
            return Person.search(person_name)[0]

    def com_net_trakt_get_tv(self, tv_show_name):
        return TVShow(tv_show_name)

    def com_net_trakt_add_tvshow(self, tv_show):
        TVShow(tv_show).add_to_library()

    def com_net_trakt_user_movie_collection(self, user_name):
        return User(user_name).movie_collection
