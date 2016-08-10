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
from NetflixRoulette import *


def MK_Common_Metadata_NetflixRoulette_Get_All_Data(media_title, media_year=None):
    if movie_year is None:
        return get_all_data(media_title)
    else:
        return get_all_data(media_title, media_year)


def MK_Common_Metadata_NetflixRoulette_Get_Id(media_title):
    return get_netflix_id(media_title)


def MK_Common_Metadata_NetflixRoulette_Get_Director(media_title):
    return get_media_director(media_title)


def MK_Common_Metadata_NetflixRoulette_Get_Summary(media_title):
    return get_media_summary(media_title)


def MK_Common_Metadata_NetflixRoulette_Get_Category(media_title):
    return get_media_category(media_title)


def MK_Common_Metadata_NetflixRoulette_Get_Cast(media_title):
    return get_media_cast(media_title)


def MK_Common_Metadata_NetflixRoulette_Get_Release_Year(media_title):
    return get_media_release_year(media_title)


def MK_Common_Metadata_NetflixRoulette_Get_Type(media_title):
    return get_media_type(media_title)


def MK_Common_Metadata_NetflixRoulette_Get_Media_Poster(media_title):
    return get_media_poster(media_title)


def MK_Common_Metadata_NetflixRoulette_Get_Rating(media_title):
    return get_media_rating(media_title)


def MK_Common_Metadata_NetflixRoulette_Get_Version():
    return get_version()
