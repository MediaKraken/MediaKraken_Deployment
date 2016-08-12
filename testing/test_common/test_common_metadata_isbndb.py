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
from MK_Common_Metadata_ISBNdb import *


class test_MK_Common_ISBNdb_API:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_Metadata_ISBNdb.MK_Common_ISBNdb_API()


    @classmethod
    def teardown_class(self):
        pass


# http://isbndb.com/api/v2/docs/authors
# http://isbndb.com/api/v2/json/[your-api-key]/author/richards_rowland
# def MK_Common_ISBNdb_Author(self, author_name):


# http://isbndb.com/api/v2/xml/mykey/books?q=science


# http://isbndb.com/api/v2/docs/publishers
# http://isbndb.com/api/v2/json/[your-api-key]/publisher/chapman_hall_crc
# def MK_Common_ISBNdb_Publisher(self, publisher_name):


# http://isbndb.com/api/v2/docs/subjects
# http://isbndb.com/api/v2/json/[your-api-key]/subject/brain_diseases_diagnosis


# http://isbndb.com/api/v2/docs/categories
# http://isbndb.com/api/v2/json/[your-api-key]/category/alphabetically.authors.r.i


# http://isbndb.com/api/v2/docs/prices
# http://isbndb.com/api/v2/json/[your-api-key]/prices/084930315X
# http://isbndb.com/api/v2/json/[your-api-key]/prices/9780849303159
# http://isbndb.com/api/v2/json/[your-api-key]/prices/principles_of_solid_mechanics
# def MK_Common_ISBNdb_Prices(self, book_info):


# http://isbndb.com/api/v2/docs/books
# http://isbndb.com/api/v2/json/[your-api-key]/book/084930315X
# http://isbndb.com/api/v2/json/[your-api-key]/book/9780849303159
# http://isbndb.com/api/v2/json/[your-api-key]/book/principles_of_solid_mechanics
# def MK_Common_ISBNdb_Books(self, book_info):
