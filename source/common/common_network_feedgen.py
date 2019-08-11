"""
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
"""

from feedgen.feed import FeedGenerator


class CommonNetworkFeedgen:
    """
    For setting up rss feeds
    """

    def __init__(self):
        self.feedgen_connection = FeedGenerator()
        self.feedgen_connection.id('http://lernfunk.de/media/654321')
        self.feedgen_connection.title('MediaKraken Notification Feed')
        self.feedgen_connection.author(
            {'name': 'John Doe', 'email': 'john@example.de'})
        self.feedgen_connection.link(
            href='http://example.com', rel='alternate')
        self.feedgen_connection.logo('http://ex.com/logo.jpg')
        self.feedgen_connection.subtitle('This is a cool feed!')
        self.feedgen_connection.link(
            href='http://larskiesow.de/test.atom', rel='self')
        self.feedgen_connection.language('en')
