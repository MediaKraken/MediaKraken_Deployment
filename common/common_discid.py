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
import discid
from libdiscid import read

# uh, what about the python-cddb stuff I have


def com_discid_default_device():
    """
    Determine default rom drive to use and grab the discid from inserted disc
    """
    discid.get_default_device()
    disc = discid.read()
    logging.info("id: %s", disc.id)
    logging.info("submission url:\n%s", disc.submission_url)
    return discid

def com_discid_caclulate_dir(dir_to_calculate):
    """
    Calculate the discid from specified directory
    """
    last = 15  # number of files in directory could be used
    sectors = 258725
    offsets = [150, 17510, 235590]
    disc = discid.put(1, last, sectors, offsets)
    logging.info("id: %s", disc.id)
    last_track = disc.tracks[disc.last_track_num - 1]
    logging.info("last track length: %s seconds", last_track.seconds)
    return disc

def com_discid_spec_device(device_id):
    #return read(device=u'/dev/cdrom1')
    return read(device=device_id)
