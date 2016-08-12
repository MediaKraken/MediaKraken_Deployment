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
from com_Emby import *


# determine install directory
@pytest.mark.parametrize(("dir_name"), [
    (None),
    #("./cache"), #TODO valid dir
    ("./cache_fake")])
def Test_com_Emby_Installed_Directory(dir_name):
    com_Emby_Installed_Directory(dir_name)


# fetch library list
@pytest.mark.parametrize(("dir_name"), [
    (None),
    #("./cache"), #TODO valid dir
    ("./cache_fake")])
def Test_com_Emby_Library_List(dir_name):
    com_Emby_Library_List(dir_name)


# check for running instance
def Test_com_Emby_Check_Instance():
    com_Emby_Check_Instance()


# C# guid to text
# def com_Emby_GUID_To_UUID(emby_guid):


# text uuid to C# guid
# def com_Emby_UUID_to_GUID(emby_guid):
