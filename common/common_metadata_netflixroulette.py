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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from NetflixRoulette import *


def common_metadata_netflixroulette_get_all_data(media_title, media_year=None):
    """
    Get all data for title and year if available
    """
    if movie_year is None:
        return get_all_data(media_title)
    else:
        return get_all_data(media_title, media_year)


def common_metadata_netflixroulette_get_id(media_title):
    """
    Get id by name
    """
    return get_netflix_id(media_title)


def common_metadata_netflixroulette_get_director(media_title):
    """
    Get director by title
    """
    return get_media_director(media_title)


def common_metadata_netflixroulette_get_summary(media_title):
    """
    Get summary by title
    """
    return get_media_summary(media_title)


def common_metadata_netflixroulette_get_category(media_title):
    """
    Get category by title
    """
    return get_media_category(media_title)


def common_metadata_netflixroulette_get_cast(media_title):
    """
    Get cast by title
    """
    return get_media_cast(media_title)


def common_metadata_netflixroulette_get_release_year(media_title):
    """
    Get release year
    """
    return get_media_release_year(media_title)


def common_metadata_netflixroulette_get_type(media_title):
    """
    Get type by name
    """
    return get_media_type(media_title)


def common_metadata_netflixroulette_get_media_poster(media_title):
    """
    Get media poster
    """
    return get_media_poster(media_title)


def common_metadata_netflixroulette_get_rating(media_title):
    """
    Get rating
    """
    return get_media_rating(media_title)


def common_metadata_netflixroulette_get_version():
    """
    Get version
    """
    return get_version()
