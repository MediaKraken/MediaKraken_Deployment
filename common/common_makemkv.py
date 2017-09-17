'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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
import subprocess


# info on inserted disk in drive 0
# makemkvcon info disc:0

'''
Operation successfully completed
Total 4 titles
Title  0
0 Video Mpeg2
1 Audio Dolby Digital
2 Audio Dolby Digital
3 Audio Dolby Digital
4 Audio Dolby Digital
5 Subtitles Dvd Subtitles
6 Subtitles Dvd Subtitles
7 Subtitles Dvd Subtitles
8 Subtitles Dvd Subtitles
9 Subtitles Dvd Subtitles

Title  1
0 Video Mpeg2
1 Audio Dolby Digital
2 Subtitles Dvd Subtitles
3 Subtitles Dvd Subtitles
4 Subtitles Dvd Subtitles

Title  2
0 Video Mpeg2
1 Audio Dolby Digital
2 Audio Dolby Digital
3 Audio Dolby Digital
4 Subtitles Dvd Subtitles
5 Subtitles Dvd Subtitles

Title  3
0 Video Mpeg2
1 Audio Dolby Digital
2 Audio Dolby Digital
3 Audio Dolby Digital
4 Subtitles Dvd Subtitles
5 Subtitles Dvd Subtitles
'''

# title 0 to path
# makemkvcon mkv disc:0 0 .
# makemkvcon --progress=-same mkv disc:0 0 .
## Current action: Saving to MKV file
'''
Current progress - 100%  , Total progress - 100%
1 titles saved
Copy complete. 1 titles saved.
'''