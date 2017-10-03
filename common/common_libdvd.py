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

import logging # pylint: disable=W0611

import dvdread
#help(dvdread.DVD)

with dvdread.DVD("/dev/sr0") as d:
    d.Open()
    print("Number of titles on disc: %d" % d.NumberOfTitles)
    for tt in range(1, d.NumberOfTitles):
        t = d.GetTitle(tt)
        #print(d.GetName())
        print(d.GetNameTitleCase()) # this gives "better" name
        print("Title %d has %d angles, %d audio tracks, %d chapters, %d subpictures, and runs for %s"
              % (t.TitleNum, t.NumberOfAngles, t.NumberOfAudios, t.NumberOfChapters,
              t.NumberOfSubpictures, t.PlaybackTimeFancy))
