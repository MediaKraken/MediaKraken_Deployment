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
import pytest  # pylint: disable=W0611
import sys

sys.path.append('.')
from common import common_metadata_netflixroulette


# @pytest.mark.parametrize(("media_title", "media_year"), [
#     ("Die Hard", None),
#     ("fakezzzzzz", None),
#     ("Red", None),
#     ("Robocop", 1987)])
# def test_com_meta_flix_get_all_data(media_title, media_year):
#     """
#     Test function
#     """
#     common_metadata_netflixroulette.com_meta_flix_get_all_data(media_title, media_year)
#
#
# @pytest.mark.parametrize(("media_title"), [
#     ("Die Hard"),
#     ("fakezzzzzz"),
#     ("Red")])
# def test_com_meta_flix_get_id(media_title):
#     """
#     Test function
#     """
#     common_metadata_netflixroulette.com_meta_flix_get_id(media_title)
#
#
# @pytest.mark.parametrize(("media_title"), [
#     ("Die Hard"),
#     ("fakezzzzzz"),
#     ("Red")])
# def test_com_meta_flix_get_director(media_title):
#     """
#     Test function
#     """
#     common_metadata_netflixroulette.com_meta_flix_get_director(media_title)
#
#
# @pytest.mark.parametrize(("media_title"), [
#     ("Die Hard"),
#     ("fakezzzzzz"),
#     ("Red")])
# def test_com_meta_flix_get_summary(media_title):
#     """
#     Test function
#     """
#     common_metadata_netflixroulette.com_meta_flix_get_summary(media_title)
#
#
# @pytest.mark.parametrize(("media_title"), [
#     ("Die Hard"),
#     ("fakezzzzzz"),
#     ("Red")])
# def test_com_meta_flix_get_category(media_title):
#     """
#     Test function
#     """
#     common_metadata_netflixroulette.com_meta_flix_get_category(media_title)
#
#
# @pytest.mark.parametrize(("media_title"), [
#     ("Die Hard"),
#     ("fakezzzzzz"),
#     ("Red")])
# def test_com_meta_flix_get_cast(media_title):
#     """
#     Test function
#     """
#     common_metadata_netflixroulette.com_meta_flix_get_cast(media_title)
#
#
# @pytest.mark.parametrize(("media_title"), [
#     ("Die Hard"),
#     ("fakezzzzzz"),
#     ("Red")])
# def test_com_meta_flix_get_release_year(media_title):
#     """
#     Test function
#     """
#     common_metadata_netflixroulette.com_meta_flix_get_release_year(media_title)
#
#
# @pytest.mark.parametrize(("media_title"), [
#     ("Die Hard"),
#     ("fakezzzzzz"),
#     ("Red")])
# def test_com_meta_flix_get_type(media_title):
#     """
#     Test function
#     """
#     common_metadata_netflixroulette.com_meta_flix_get_type(media_title)
#
#
# @pytest.mark.parametrize(("media_title"), [
#     ("Die Hard"),
#     ("fakezzzzzz"),
#     ("Red")])
# def test_com_meta_flix_get_media_poster(media_title):
#     """
#     Test function
#     """
#     common_metadata_netflixroulette.com_meta_flix_get_media_poster(media_title)
#
#
# @pytest.mark.parametrize(("media_title"), [
#     ("Die Hard"),
#     ("fakezzzzzz"),
#     ("Red")])
# def test_com_meta_flix_get_rating(media_title):
#     """
#     Test function
#     """
#     common_metadata_netflixroulette.com_meta_flix_get_rating(media_title)
#
#
# def test_com_meta_flix_get_version():
#     """
#     Test function
#     """
#     common_metadata_netflixroulette.com_meta_flix_get_version()
