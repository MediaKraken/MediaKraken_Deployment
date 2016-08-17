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
import os
import sys
sys.path.append("./vault/lib")
from babelfish import Language
import subliminal


def com_meta_fetch_subtitle(file_name, sub_lang="en"):
    """
    # fetch subtitles
    """
    #file_hash = com_Hash.com_hash_thesubdb(file_name)
    command_handle = os.popen("subliminal -l " + sub_lang + " -- \'" + file_name.encode("utf8") + "\'")
    cmd_output = command_handle.read()
    return cmd_output


def com_meta_fetch_subtitle_batch(dir_name, sub_lang):
    """
    # batch fetch subtitles
    """
    # configure the cache
#    subliminal.cache_region.configure('dogpile.cache.dbm', arguments={'filename': '/home/spoot/cachefile.dbm'})
#    # scan for videos in the folder and their subtitles
#    videos = subliminal.scan_videos(['/nfsmount/TV_Shows_Misc/Earth 2
    #(1994)/season 1/'], subtitles=True, embedded_subtitles=True)
#    # download
#    subliminal.download_best_subtitles(videos, Language('eng'))
    pass
