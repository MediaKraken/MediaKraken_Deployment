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
import logging
from feedgen.feed import FeedGenerator


class MK_Common_Feedgen_API:
    def __init__(self):
        self.fg = FeedGenerator()
        self.fg.id('http://lernfunk.de/media/654321')
        self.fg.title('Metaman Notification Feed')
        self.fg.author({'name':'John Doe', 'email':'john@example.de'})
        self.fg.link(href='http://example.com', rel='alternate')
        self.fg.logo('http://ex.com/logo.jpg')
        self.fg.subtitle('This is a cool feed!')
        self.fg.link(href='http://larskiesow.de/test.atom', rel='self')
        self.fg.language('en')
