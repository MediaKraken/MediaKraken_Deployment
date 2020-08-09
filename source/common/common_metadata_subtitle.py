"""
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
"""

from datetime import timedelta

from babelfish import Language
from subliminal import download_best_subtitles, region, save_subtitles, scan_videos

# configure the cache
region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefile.dbm'})

# scan for videos newer than 2 weeks and their existing subtitles in a folder
videos = scan_videos('/video/folder', age=timedelta(weeks=2))

# download best subtitles
subtitles = download_best_subtitles(videos, {Language('eng'), Language('fra')})

# save them to disk, next to the video
for v in videos:
    save_subtitles(v, subtitles[v])
