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

import logging
import discid

# uh, what about the python-cddb stuff I have

# grab discid from default device
def MK_Common_DiscID_Default_Device():
    discid.get_default_device()
    disc = discid.read()
    logging.debug("id: %s" % disc.id)
    logging.debug("submission url:\n%s" % disc.submission_url)
    return discid


# calculate discid from directory
def MK_Common_DiskID_Caclulate_Dir(dir_to_calculate):
    last = 15  # number of files in directory could be used
    sectors = 258725
    offsets = [150, 17510, 235590]
    disc = discid.put(1, last, sectors, offsets)
    logging.debug("id: %s" % disc.id)
    last_track = disc.tracks[disc.last_track_num - 1]
    logging.debug("last track length: %s seconds" % last_track.seconds)
    return disc
