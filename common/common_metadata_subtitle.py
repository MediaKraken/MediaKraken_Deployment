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
import logging
import os
import sys
import re
import MK_Common_File
import MK_Common_Hash
sys.path.append("../../MediaKraken_Common/lib")
from babelfish import Language
import subliminal


# fetch subtitles
def MK_Common_Metadata_Fetch_Subtitle(file_name, sub_lang="en"):
    #file_hash = MK_Common_Hash.MK_Common_Hash_TheSubDB(file_name)
    f = os.popen("subliminal -l " + sub_lang + " -- \'" + file_name.encode("utf8") + "\'")
    cmd_output = f.read()
    return cmd_output


# batch fetch subtitles
def MK_Common_Metadata_Fetch_Subtitle_Batch(dir_name, sub_lang):
    # configure the cache
#    subliminal.cache_region.configure('dogpile.cache.dbm', arguments={'filename': '/home/spoot/cachefile.dbm'})
#    # scan for videos in the folder and their subtitles
#    videos = subliminal.scan_videos(['/nfsmount/TV_Shows_Misc/Earth 2 (1994)/season 1/'], subtitles=True, embedded_subtitles=True)
#    # download
#    subliminal.download_best_subtitles(videos, Language('eng'))
    pass
