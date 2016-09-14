'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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
import subprocess
import logging


class TestSubprogramChapterImage(object):
    """
    Test create chapter image
    """

    def test_sub_chapter_image(self):
        """
        Test function
        """
        self.proc_info = subprocess.Popen(['./subprogram_create_chapter_images'], shell=False)
        logging.info("PID: %s", self.proc_info.pid)
        self.proc_info.wait()
