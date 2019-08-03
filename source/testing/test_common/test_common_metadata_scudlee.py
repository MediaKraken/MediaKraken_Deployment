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

import sys

sys.path.append('.')
from common import common_metadata_scudlee


def test_mk_scudlee_fetch_xml():
    """
    grab the data from github
    """
    common_metadata_scudlee.mk_scudlee_fetch_xml()


def test_mk_scudlee_anime_list_parse(file_name=None):
    """
    # parse the anime list
    """
    common_metadata_scudlee.mk_scudlee_anime_list_parse()


def test_mk_scudlee_anime_set_parse(file_name=None):
    """
    # parse the movieset list
    """
    common_metadata_scudlee.mk_scudlee_anime_set_parse()
