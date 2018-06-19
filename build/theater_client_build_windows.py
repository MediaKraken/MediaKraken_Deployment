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

import os
import shutil
import sys

sys.path.append('../MediaKraken-PyLint/build_code/jenkins/')
import pipeline_packages_list

# nuke previous pyinstaller directories to start fresh
try:
    shutil.rmtree('C:\\Users\\jenkinsbuild\\Documents\\github\\build')
except:
    pass
try:
    shutil.rmtree('C:\\Users\\jenkinsbuild\\Documents\\github\\dist')
except:
    pass

# start building python "app"
os.system('pyinstaller --clean'
          ' C:\\Users\\jenkinsbuild\\Documents\\github\\main_server.py')

# start building python programs
for app_to_build in pipeline_packages_list.PIPELINE_APP_LIST:
    os.system('pyinstaller --clean C:\\Users\\jenkinsbuild\\Documents\\github\\'
              + app_to_build + '.py')
