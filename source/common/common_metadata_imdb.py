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

from imdbpie import Imdb


class CommonMetadataIMDB:
    """
    Class for interfacing with imdb
    """

    def __init__(self, cache=True, cache_dir=None):
        # open connection to imdb
        if cache is not None:
            if cache_dir is not None:
                self.imdb = Imdb(cache=True, cache_dir=cache_dir)
            else:
                self.imdb = Imdb(cache=True)
        else:
            self.imdb = Imdb()

    def com_imdb_title_search(self, media_title):
        """
        # fetch info from title
        """
        return self.imdb.search_for_title(media_title)

    def com_imdb_id_search(self, media_id):
        """
        # fetch info by ttid
        """
        return self.imdb.get_title_by_id(media_id)

    def com_imdb_person_by_id(self, person_id):
        """
        # fetch person info by id
        """
        return self.imdb.get_person_by_id(person_id)

    def com_imdb_person_images_by_id(self, person_id):
        """
        # fetch person images by id
        """
        return self.imdb.get_person_images(person_id)

    def com_imdb_title_review_by_id(self, media_id):
        """
        # fetch the title review
        """
        return self.imdb.get_title_reviews(media_id)
