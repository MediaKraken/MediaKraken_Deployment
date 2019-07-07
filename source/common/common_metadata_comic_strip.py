'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

# https://github.com/MediaKraken-Dep/dosage
import subprocess
from shlex import split

'''
positional arguments:
  comic                 comic module name (including case insensitive
                        substrings)

optional arguments:
  -v, --verbose         provides verbose output, use multiple times for more
                        verbosity
  -n NUMSTRIPS, --numstrips NUMSTRIPS
                        traverse and retrieve the given number of comic
                        strips; use --all to retrieve all comic strips
  -a, --all             traverse and retrieve all comic strips
  -c, --continue        traverse and retrieve comic strips until an existing
                        one is found
  -b PATH, --basepath PATH
                        set the path to create individual comic directories
                        in, default is Comics
  --baseurl PATH        the base URL of your comics directory (for RSS, HTML,
                        etc.); this should correspond to --base-path
  -l, --list            list available comic modules
  --singlelist          list available comic modules in a single list
  -m, --modulehelp      display help for comic modules
  -t, --timestamps      print timestamps for all output at any info level
  -o {html,json,rss}, --output {html,json,rss}
                        sets output handlers for downloaded comics
  --adult               confirms that you are old enough to view adult content
'''


class CommonMetadataComicStrip:
    """
    Class for snagging comic strips
    """

    def __init__(self, base_path):
        self.base_path = base_path

    def com_meta_com_list_strips(self, adult_access=False):
        if adult_access:
            return subprocess.check_output(
                split('dosage -b %s --singlelist --adult', (self.base_path,)))
        else:
            return subprocess.check_output(split('dosage -b %s --singlelist', (self.base_path,)))

    def com_meta_com_fetch_strip(self, strip_name, adult_access=False):
        if adult_access:
            return subprocess.check_output(split('dosage -b %b %s', (self.base_path, strip_name,)))
        else:
            return subprocess.check_output(
                split('dosage -b %s %s --adult', (self.base_path, strip_name,)))

    def com_meta_com_current_fetch(self, adult_access=False):
        if adult_access:
            return subprocess.check_output(split('dosage -b %s @', (self.base_path,)))
        else:
            return subprocess.check_output(split('dosage -b %s @ --adult', (self.base_path,)))
