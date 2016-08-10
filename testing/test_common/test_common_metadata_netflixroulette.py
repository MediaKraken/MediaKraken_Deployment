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


import pytest
import sys
sys.path.append("../common")
from MK_Common_Metadata_NetflixRoulette import *


@pytest.mark.parametrize(("media_title", "media_year"), [
    ("Die Hard", None),
    ("fakezzzzzz", None),
    ("Red", None),
    ("Robocop", 1987)])
def test_MK_Common_Metadata_NetflixRoulette_Get_All_Data(media_title, media_year):
    MK_Common_Metadata_NetflixRoulette_Get_All_Data(media_title, media_year)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def test_MK_Common_Metadata_NetflixRoulette_Get_Id(media_title):
    MK_Common_Metadata_NetflixRoulette_Get_Id(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def test_MK_Common_Metadata_NetflixRoulette_Get_Director(media_title):
    MK_Common_Metadata_NetflixRoulette_Get_Director(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def test_MK_Common_Metadata_NetflixRoulette_Get_Summary(media_title):
    MK_Common_Metadata_NetflixRoulette_Get_Summary(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def test_MK_Common_Metadata_NetflixRoulette_Get_Category(media_title):
    MK_Common_Metadata_NetflixRoulette_Get_Category(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def test_MK_Common_Metadata_NetflixRoulette_Get_Cast(media_title):
    MK_Common_Metadata_NetflixRoulette_Get_Cast(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def test_MK_Common_Metadata_NetflixRoulette_Get_Release_Year(media_title):
    MK_Common_Metadata_NetflixRoulette_Get_Release_Year(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def test_MK_Common_Metadata_NetflixRoulette_Get_Type(media_title):
    MK_Common_Metadata_NetflixRoulette_Get_Type(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def test_MK_Common_Metadata_NetflixRoulette_Get_Media_Poster(media_title):
    MK_Common_Metadata_NetflixRoulette_Get_Media_Poster(media_title)


@pytest.mark.parametrize(("media_title"), [
    ("Die Hard"),
    ("fakezzzzzz"),
    ("Red")])
def test_MK_Common_Metadata_NetflixRoulette_Get_Rating(media_title):
    MK_Common_Metadata_NetflixRoulette_Get_Rating(media_title)


def test_MK_Common_Metadata_NetflixRoulette_Get_Version():
    MK_Common_Metadata_NetflixRoulette_Get_Version()

