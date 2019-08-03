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

import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
from common import common_config_ini
from common import common_network_trakt


class TestCommonTrakt:

    @classmethod
    def setup_class(self):
        # open the database
        option_config_json, db_connection = common_config_ini.com_config_read(db_prod=False)
        self.trakt_connection = common_network_trakt.CommonNetworkTrakt(
            option_config_json)

    @classmethod
    def teardown_class(self):
        pass

    # class com_Trakt_API:
    #    def __init__(self, response):

    # calendar by days
    @pytest.mark.parametrize(("day_count"), [
        (7),
        (400)])
    def test_com_trakt_calendar_by_days(self, day_count):
        """
        Test function
        """
        self.trakt_connection.com_net_trakt_calendar_by_days(day_count)

    # dismiss recommendation
#    def com_trakt_dismiss_recommendation(imdb_id, imdb_title, imdb_year):
