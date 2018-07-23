'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

# https://pypi.org/project/rarfile/

# needs unrar to be available

import rarfile

rf = rarfile.RarFile('myarchive.rar')
for f in rf.infolist():
    print f.filename, f.file_size
    if f.filename == 'README':
        print(rf.read(f))


with rarfile.RarFile('archive.rar') as rf:
    with rf.open('README') as f:
        for ln in f:
            print(ln.strip())
