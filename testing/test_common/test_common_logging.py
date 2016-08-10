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
sys.path.append("../MediaKraken_Common")
from MK_Common_Logging import *


# def MK_Common_Logging_Start(log_name="./log/MediaKraken_Main"):
@pytest.mark.parametrize(("log_name"), [
    (None),
    ("./log/MediaKraken_Test"),
    ("./log_fake/MediaKraken_Test")])
def test_MK_Common_Logging_Start(log_name):
    MK_Common_Logging_Start(log_name)
