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

import subprocess
import logging


# determine video attributes
def MK_Common_FFMPEG_Media_Attr(file_path):
    """
    Runs ffprobe to generate the media file specifications which is returned in json
    """
    logging.debug("ffmpeg attr: %s", file_path)
    try:
        media_json = subprocess.check_output(['ffprobe', '-show_format', '-show_streams', \
            '-show_chapters', '-loglevel', 'quiet', '-print_format', 'json', file_path])
    except:
        media_json = None
    return media_json
