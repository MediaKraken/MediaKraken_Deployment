"""
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
"""

import dvdread


# help(dvdread.DVD)

def com_dvd_read_titles(drive_name):
    """
    Read the titles for selected drive name
    """
    track_data = []
    with dvdread.DVD(drive_name) as disk_handle:
        disk_handle.Open()
        for ndx in range(1, disk_handle.NumberOfTitles):
            disk_title = disk_handle.GetTitle(ndx)
            track_data.append(
                (disk_handle.GetNameTitleCase(), disk_title.TitleNum,
                 disk_title.NumberOfAngles, disk_title.NumberOfAudios,
                 disk_title.NumberOfChapters, disk_title.NumberOfSubpictures,
                 disk_title.PlaybackTimeFancy))
    return track_data
