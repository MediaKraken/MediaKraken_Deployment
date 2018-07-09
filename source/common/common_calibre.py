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

import subprocess


# notes on how to use the cli for the apps
# https://manual.calibre-ebook.com/generated/en/cli-index.html


def com_calibre_convert_ebook(target_file, target_format):
    # TODO shelix for little bobby tables
    calibre_pid = subprocess.Popen(
        ['./bin/calibre/ebook-convert', target_file, target_format])
    return calibre_pid
