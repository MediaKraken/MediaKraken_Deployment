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
import logging # pylint: disable=W0611
from . import common_network


# code to use
# http://www.tvmaze.com/api


class CommonMetadatatvmaze(object):
    """
    Class for interfacing with tvmaze
    """
    def __init__(self):
        self.API_BASE_URL = 'http://api.tvmaze.com/'


    def com_meta_tvmaze_show_list(self, page_no=0):
        """
        # show list 50 per page - 0 is first page
        """
        url_opts = page_no,
        return common_network.mk_network_fetch_from_url((self.API_BASE_URL + 'shows?page=%s'\
            % url_opts), None)


    def com_meta_tvmaze_show_updated(self):
        """
        # show when last updated
        """
        # returns id's and timestamps of last changed
        return common_network.mk_network_fetch_from_url(\
            self.API_BASE_URL + 'updates/shows', None)


    def com_meta_tvmaze_widesearch(self, show_name, show_year=None):
        """
        # lookup show
        """
        url_opts = show_name,
        return common_network.mk_network_fetch_from_url((self.API_BASE_URL + 'search/shows?q=%s'\
            % url_opts), None)


    def com_meta_tvmaze_narrowsearch(self, show_name, show_year=None):
        """
        # lookup specific show
        """
        url_opts = show_name,
        return common_network.mk_network_fetch_from_url((\
            self.API_BASE_URL + 'singlesearch/shows?q=%s' % url_opts), None)


    def com_meta_tvmaze_show_by_id(self, tvmaze_id, tvrage_id, imdb_id, tvdb_id,\
            embed_info=True):
        """
        # lookup specific id
        """
        result_json = None
        # tvmaze lookup and fetch embed info if needed
        if tvmaze_id is not None:
            url_opts = tvmaze_id,
            if embed_info:
                result_json = common_network.mk_network_fetch_from_url((\
                    self.API_BASE_URL + 'shows/%s?embed[]=episodes&embed[]=cast'\
                    % url_opts), None)
            else:
                result_json = common_network.mk_network_fetch_from_url((\
                    self.API_BASE_URL + 'shows/%s' % url_opts), None)
        else:
            # currently embed options don't work on the lookup calls
            if tvrage_id is not None and result_json is None:
                url_opts = tvrage_id,
                result_json = common_network.mk_network_fetch_from_url((\
                    self.API_BASE_URL + 'lookup/shows?tvrage=%s' % url_opts), None)
            elif imdb_id is not None and result_json is None:
                url_opts = imdb_id,
                result_json = common_network.mk_network_fetch_from_url((\
                    self.API_BASE_URL + 'lookup/shows?imdb=%s' % url_opts), None)
            elif tvdb_id is not None and result_json is None:
                url_opts = tvdb_id,
                result_json = common_network.mk_network_fetch_from_url((\
                    self.API_BASE_URL + 'lookup/shows?thetvdb=%s' % url_opts), None)
            if embed_info and result_json is not None:
                result_json = self.com_meta_tvmaze_show_by_id(self, result_json['id'], None,\
                    None, None, True)
        return result_json


    def com_meta_tvmaze_person_by_name(self, person_name):
        """
        # people search (doesnt' appear to have episode data here)
        """
        url_opts = person_name,
        return common_network.mk_network_fetch_from_url(self.API_BASE_URL + 'search/people?q=%s'\
            % url_opts)


    def com_meta_tvmaze_schedule(self, country_code=None, schedule_date=None):
        """
        # schedule
        """
        result_json = common_network.mk_network_fetch_from_url(self.API_BASE_URL + 'schedule',\
            None)
        result_json = common_network.mk_network_fetch_from_url(\
            self.API_BASE_URL + 'schedule?country=US&date=2014-12-01', None)
        result_json = common_network.mk_network_fetch_from_url(\
            self.API_BASE_URL + 'schedule/full', None)
        return result_json
