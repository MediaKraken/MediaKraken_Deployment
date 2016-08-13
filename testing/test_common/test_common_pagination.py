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
from common_pagination import *


def test_get_css_framework():
    get_css_framework()


def test_get_link_size():
    get_link_size()


def test_show_single_page_or_not():
    show_single_page_or_not()


@pytest.mark.parametrize(("client_items_per_page"), [
    (None), # defualt to 30
    (50)])
def test_get_page_items(client_items_per_page):
    get_page_items(client_items_per_page)


# def get_pagination(**kwargs):
