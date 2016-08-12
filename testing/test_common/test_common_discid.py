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
from MK_Common_DISCID import *


# grab discid from default device
def Test_MK_Common_DiscID_Default_Device():
    MK_Common_DiscID_Default_Device()


# calculate discid from directory
@pytest.mark.parametrize(("dir_to_calculate"), [
    ("./cache"),
    ("./cache_fake")])
def Test_MK_Common_DiskID_Caclulate_Dir(dir_to_calculate):
    MK_Common_DiskID_Caclulate_Dir(dir_to_calculate)
