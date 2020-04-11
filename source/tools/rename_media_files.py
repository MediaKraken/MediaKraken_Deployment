"""
  Copyright (C) 2019 Quinn D Granfor <spootdev@gmail.com>

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

import os
from os import walk  # pylint: disable=C0412

from guessit import guessit

media_files = 0
for root, dirs, files in walk('X:\\zz_movie'):
    for file_name_loop in files:
        filename, file_extension = os.path.splitext(file_name_loop)
        if file_extension in ('.mkv', '.mp4', '.iso'):
            guessit_name = guessit(file_name_loop)
            if 'title' in guessit_name:
                if 'year' in guessit_name:
                    media_files += 1
                    print(filename, ':',
                          guessit_name['title'] + ' (' + str(guessit_name['year']) + ')', flush=True)
                    user_answer = input('Should I rename/move it?')
                    if user_answer == 'y':
                        os.rename(os.path.join(root, file_name_loop), os.path.join(
                            'X:\\zz_movie', guessit_name['title']
                                            + ' (' + str(
                                guessit_name['year']) + ')' + file_extension))
                        # print(os.path.join(root, file_name_loop), flush=True)
            else:
                print(filename, flush=True)
                print(root, flush=True)
                guessit_name = guessit(root)
                if 'title' in guessit_name:
                    if 'year' in guessit_name:
                        media_files += 1
                        print(root, ':',
                              guessit_name['title'] + ' (' + str(guessit_name['year']) + ')', flush=True)
                        user_answer = input('Should I rename/move it?')
                        if user_answer == 'y':
                            os.rename(os.path.join(root, filename + file_extension), os.path.join(
                                'X:\\zz_movie', guessit_name['title']
                                                + ' (' + str(
                                    guessit_name['year']) + ')' + file_extension))
print(media_files, flush=True)
