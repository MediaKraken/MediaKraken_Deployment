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

import omdb


class CommonMetadataOMDB(object):
    """
    Class for interfacing with omdb
    """

    def __init__(self):
        pass

    def com_omdb_get(self, media_title, media_year, media_fullplot, media_tomatoes):
        omdb.get(title=media_title, year=media_year, fullplot=media_fullplot,
                 tomatoes=media_tomatoes)

    def com_omdb_search(self, media_title):
        """
        Search
        """
        omdb.search(media_title)

    def com_omdb_search_movie(self, media_title):
        """
        Search movie
        """
        omdb.search_movie(media_title)

    def com_omdb_search_episode(self, media_title):
        """
        Search episode
        """
        omdb.search_episode(media_title)

    def com_omdb_search_series(self, media_title):
        """
        Search series
        """
        omdb.search_series(media_title)

    def com_omdb_imdb(self, imdbid):
        """
        Info by IMDB id
        """
        omdb.imdbid(imdbid)

    def com_omdb_title(self, media_title):
        """
        Grab by title
        """
        omdb.title(media_title)

    def com_omdb_default(self):
        """
        Set defaults for data returned
        """
        omdb.set_default('tomatoes', True)

    def com_omdb_request(self, media_title, media_year, media_fullplot, media_tomatoes):
        omdb.request(media_title, media_year, media_fullplot, media_tomatoes)
