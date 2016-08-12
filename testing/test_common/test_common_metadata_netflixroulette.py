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
import pytest
import sys
sys.path.append("../common")
from common_metadata_netflixroulette import *


@pytest.mark.parametrize(("media_title", "media_year"), [
    ("Die Hard", None),
    ("fakezzzzzz", None),
    ("Red", None),
    ("Robocop", 1987)])
def Test_common_metadata_netflixroulette_Get_All_Data(media_title, media_year):
    common_metadata_netflixroulette_Get_All_Data(media_title, media_year)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def Test_common_metadata_netflixroulette_Get_Id(media_title):
    common_metadata_netflixroulette_Get_Id(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def Test_common_metadata_netflixroulette_Get_Director(media_title):
    common_metadata_netflixroulette_Get_Director(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def Test_common_metadata_netflixroulette_Get_Summary(media_title):
    common_metadata_netflixroulette_Get_Summary(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def Test_common_metadata_netflixroulette_Get_Category(media_title):
    common_metadata_netflixroulette_Get_Category(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def Test_common_metadata_netflixroulette_Get_Cast(media_title):
    common_metadata_netflixroulette_Get_Cast(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def Test_common_metadata_netflixroulette_Get_Release_Year(media_title):
    common_metadata_netflixroulette_Get_Release_Year(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def Test_common_metadata_netflixroulette_Get_Type(media_title):
    common_metadata_netflixroulette_Get_Type(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def Test_common_metadata_netflixroulette_Get_Media_Poster(media_title):
    common_metadata_netflixroulette_Get_Media_Poster(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def Test_common_metadata_netflixroulette_Get_Rating(media_title):
    common_metadata_netflixroulette_Get_Rating(media_title)


def Test_common_metadata_netflixroulette_Get_Version():
    common_metadata_netflixroulette_Get_Version()

