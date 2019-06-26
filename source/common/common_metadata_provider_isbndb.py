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

import requests

from . import common_network


class CommonMetadataISBNdb:
    """
    Class for interfacing with isbndb
    """

    def __init__(self, option_config_json):
        self.api_key = option_config_json['API']['isbndb']

    # http://isbndb.com/api/v2/docs/authors
    # http://isbndb.com/api/v2/json/[your-api-key]/author/richards_rowland
    def com_isbndb_author(self, author_name):
        """
        Grab the author
        """
        return common_network.mk_network_fetch_from_url('http://isbndb.com/api/v2/json/'
                                                        + self.api_key + '/author/' + author_name,
                                                        None)

    # http://isbndb.com/api/v2/xml/mykey/books?q=science

    # http://isbndb.com/api/v2/docs/publishers
    # http://isbndb.com/api/v2/json/[your-api-key]/publisher/chapman_hall_crc
    def com_isbndb_publisher(self, publisher_name):
        """
        Grab the publisher
        """
        return common_network.mk_network_fetch_from_url('http://isbndb.com/api/v2/json/'
                                                        + self.api_key + '/publisher/'
                                                        + publisher_name, None)

    # http://isbndb.com/api/v2/docs/subjects
    # http://isbndb.com/api/v2/json/[your-api-key]/subject/brain_diseases_diagnosis

    # http://isbndb.com/api/v2/docs/categories
    # http://isbndb.com/api/v2/json/[your-api-key]/category/alphabetically.authors.r.i

    # http://isbndb.com/api/v2/docs/prices
    # http://isbndb.com/api/v2/json/[your-api-key]/prices/084930315X
    # http://isbndb.com/api/v2/json/[your-api-key]/prices/9780849303159
    # http://isbndb.com/api/v2/json/[your-api-key]/prices/principles_of_solid_mechanics
    def com_isbndb_prices(self, book_info):
        """
        Grab prices
        """
        return common_network.mk_network_fetch_from_url('http://isbndb.com/api/v2/json/'
                                                        + self.api_key + '/prices/'
                                                        + book_info, None)

    # http://isbndb.com/api/v2/docs/books
    # http://isbndb.com/api/v2/json/[your-api-key]/book/084930315X
    # http://isbndb.com/api/v2/json/[your-api-key]/book/9780849303159
    # http://isbndb.com/api/v2/json/[your-api-key]/book/principles_of_solid_mechanics
    def com_isbndb_books(self, book_info):
        """
        Search
        """
        return requests.get('http://isbndb.com/api/v2/json/'
                            + self.api_key + '/book/' + book_info)
