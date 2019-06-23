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
from common import common_metadata_pitchfork


class TestCommonpitchfork:

    @classmethod
    def setup_class(self):
        self.pitchfork_connection = common_metadata_pitchfork.CommonMetadataPitchfork()

    @classmethod
    def teardown_class(self):
        pass

    @pytest.mark.parametrize(("artist_name", "album_title"), [
        ("Megadeath", "Youthanasia"),
        ("FakeBand", "FakeAlbum")])
    def test_com_pfork_search(self, artist_name, album_title):
        """
        Test function
        """
        self.pitchfork_connection.com_pfork_search(artist_name, album_title)

    def test_com_pfork_album_title(self):
        """
        Test function
        """
        self.pitchfork_connection.com_pfork_album_title()

    def test_com_pfork_album_label(self):
        """
        Test function
        """
        self.pitchfork_connection.com_pfork_album_label()

    def test_com_pfork_album_review(self):
        """
        Test function
        """
        self.pitchfork_connection.com_pfork_album_review()

    def test_com_pfork_album_cover_art_link(self):
        """
        Test function
        """
        self.pitchfork_connection.com_pfork_album_cover_art_link()

    def test_com_pfork_album_review_score(self):
        """
        Test function
        """
        self.pitchfork_connection.com_pfork_album_review_score()
