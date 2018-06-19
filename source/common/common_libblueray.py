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

import bluread


# help(bluread)

# https://github.com/cmlburnett/PyBluRead/blob/master/setup.py
# sudo apt-get install libbluray-dev

def com_bray_read_titles(drive_name):
    track_data = []
    with bluread.Bluray(drive_name) as b:
        b.Open()
        print(("Volume ID: %s" % b.VolumeId))
        print(("Org ID: %s" % b.OrgId))
        for i in range(b.NumberOfTitles):
            t = b.GetTitle(i)
            track_data.append((i, t.NumberOfAngles, t.NumberOfChapters,
                               t.NumberOfClips, t.LengthFancy))
    return track_data
