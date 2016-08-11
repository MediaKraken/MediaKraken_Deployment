'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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
import logging
import sys
from xml.dom import minidom
import MK_Common_File
import MK_Common_Network
from imdbpie import Imdb


class MK_Common_IMDB_API:
    """
    Class for interfacing with imdb
    """
    def __init__(self, cache, cache_location):
        # open connection to IMDB
        if cache is not None:
            if cache_location is not None:
                self.imdb = Imdb(cache=True, cache_dir=cache_location)
            else:
                self.imdb = Imdb(cache=True)
        else:
            self.imdb = Imdb()


    # fetch info from title
    def MK_Common_IMDB_Title_Search(self, media_title):
        return self.imdb.search_for_title(media_title)


    # fetch info by ttid
    def MK_Common_IMDB_ID_Search(self, media_id):
        return self.imdb.get_title_by_id(media_id)


    # fetch person info by id
    def MK_Common_IMDB_Person_By_ID(self, person_id):
        return self.imdb.get_person_by_id(person_id)


    # fetch person images by id
    def MK_Common_IMDB_Person_Images_By_Id(self, person_id):
        return self.imdb.get_person_images(person_id)


    # fetch the title review
    def MK_Common_IMDB_Title_Review_By_ID(self, media_id):
        return self.imdb.get_title_reviews(media_id)
