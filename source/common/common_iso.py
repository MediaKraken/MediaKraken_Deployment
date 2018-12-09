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

# https://github.com/MediaKraken-Dependancies/isoparser
import isoparser

from . import common_global


class CommonISO(object):
    """
    Class for interfacing with iso images
    """

    def __init__(self):
        self.iso_inst = None

    def com_iso_load(self, url_file):
        """
        Open the iso file for parsing (url or file)
        """
        common_global.es_inst.com_elastic_index('info', {"iso url/file": url_file})
        self.iso_inst = isoparser.parse(url_file)

    def com_iso_find_children(self, file_directory):
        return self.iso_inst.record(file_directory.split()).children

    def com_iso_read_content(self, file_directory):
        return self.iso_inst.record(file_directory.split()).content
