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
from MK_Common_Metadata_IMDB import *


class Test_MK_Common_IMDB_API:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_Metadata_IMDB.MK_Common_IMDB_API()


    @classmethod
    def teardown_class(self):
        pass


    # fetch info from title
    def test_MK_Common_IMDB_Title_Search(self):
        MK_Common_IMDB_Title_Search("Robocop")


# fetch info by ttid
# def MK_Common_IMDB_ID_Search(self, media_id):


# fetch person info by id
# def MK_Common_IMDB_Person_By_ID(self, person_id):


# fetch person images by id
# def MK_Common_IMDB_Person_Images_By_Id(self, person_id):


# fetch the title review
# def MK_Common_IMDB_Title_Review_By_ID(self, media_id):
