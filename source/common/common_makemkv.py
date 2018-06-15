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

import subprocess


def com_makemkv_drive_list():
    makemkv_pid = subprocess.Popen(['makemkvcon', '-r', '--cache=1', 'info', 'disc:9999'],
                                   stdout=subprocess.PIPE, bufsize=1)
    for line in iter(makemkv_pid.stdout.readline, b''):
        print(line)
        makemkv_pid.communicate()


def com_makemkv_rip_disc(file_location, cache_size=1024, disc=0, track='all', min_seconds=120):
    makemkv_pid = subprocess.Popen(['makemkvcon', '--noscan', '-r',
                                    ('--minlength=%s' % min_seconds),
                                    ('--cache=%s' % cache_size),
                                    ('disc:%s' % disc), track, file_location],
                                   stdout=subprocess.PIPE, bufsize=1)
    for line in iter(makemkv_pid.stdout.readline, b''):
        print(line)
        makemkv_pid.communicate()
