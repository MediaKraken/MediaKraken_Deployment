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

#from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611

'''
python3 setup.py build
python3 setup.py install

sudo apt-get install python3-pip
sudo apt-get install python3-dev
sudo pip3 install crudexml
'''

import bluread
#help(bluread)

with bluread.Bluray("/dev/sr0") as b:
    b.Open()
    print("Volume ID: %s" % b.VolumeId)
    print("Org ID: %s" % b.OrgId)
    print("Number of titles on disc: %d" % b.NumberOfTitles)
    for i in range(b.NumberOfTitles):
        t = b.GetTitle(i)
        # Filter out special features, etc.
        if t.Length < 300000000: continue
        print("Title %d has %d angles, %d chapters, %d clips, and runs for %s" % (i, t.NumberOfAngles, t.NumberOfChapters, t.NumberOfClips, t.LengthFancy))
