"""
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
"""

from common import common_file

for file_name in common_file.com_file_dir_list(
        '/home/spoot/github/MediaKraken/MediaKraken_Deployment', filter_text='py',
        walk_dir=True, skip_junk=False, file_size=False, directory_only=False):
    # print('File: %s' % file_name, flush=True)
    with open(file_name) as f_pointer:
        for file_line in f_pointer:
            if file_line.split(' ')[0] == 'def':
                # print('line: %s' % file_line, flush=True)
                # print('chunk: %s' % file_line.split(' ')[1].split('(')[0], flush=True)
                if file_line.split(' ')[1].split('(')[0].islower() is False \
                        and file_name.find('/lib/') == -1 \
                        and file_name.find('_Kodi') == -1 \
                        and file_name.find('_Roku') == -1 \
                        and file_name.find('_Tizen') == -1:
                    print(('File: %s' % file_name), flush=True)
                    print(("Upper char found: %s" %
                           file_line.split(' ')[1].split('(')[0]), flush=True)
                    command_string = 'find . -type f -name "*.py" -exec sed -i \'s/' \
                                     + file_line.split(' ')[1].split('(')[0] + '/' \
                                     + file_line.split(' ')[1].split('(')[0].lower() + '/g\' {} +'
                    print(("command: %s" % command_string), flush=True)
