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
from common import common_metadata_rotten_tomatoes


# class TestCommonMetadataRottenTomatoes(object):
#
#     @classmethod
#     def setup_class(self):
#         self.rt_connection = common_metadata_rotten_tomatoes.CommonMetadataRottenTomatoes()
#
#     @classmethod
#     def teardown_class(self):
#         pass
#
#     # search for movie title and year
#     @pytest.mark.parametrize(("movie_title", "movie_year"), [
#         ("Robocop", None),
#         ("Robocop", 1987),
#         ("Fake", None)])
#     def test_com_rt_search(self, movie_title, movie_year):
#         """
#         Test function
#         """
#         self.rt_connection.com_rt_search(movie_title, movie_year)
