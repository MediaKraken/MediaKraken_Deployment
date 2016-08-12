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
from com_Metadata_Scudlee import *


# def fetch the anime list by scudlee for thetvdb crossreference
def Test_MK_Scudlee_Fetch_XML():
    MK_Scudlee_Fetch_XML()


# parse the anime list
# def MK_Scudlee_Anime_List_Parse(file_name=None):


# parse the movieset list
# def MK_Scudlee_Anime_Set_Parse(file_name=None):
