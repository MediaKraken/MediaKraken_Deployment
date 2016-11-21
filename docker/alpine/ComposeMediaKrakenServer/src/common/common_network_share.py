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
import logging # pylint: disable=W0611
import subprocess


def com_net_share_mount(db_connection):
    # mount the share/dirs
    for share in db_connection.db_audit_shares():
        logging.info('Attempting mount of %s %s %s' % share['mm_media_share_type'], \
                     share['mm_media_share_server'], share['mm_media_share_path'])
        mount_command = []
        if share['mm_media_share_type'] == 'nfs':
            mount_command.append('mount')
            mount_command.append('-t')
            mount_command.append('nfs')
            if share['mm_media_share_user'] != 'guest':
                mount_command.append('-o')
                mount_command.append('uid=1000') # gid=1000
            mount_command.append(share['mm_media_share_server'] + ':/' + share['mm_media_share_path'])
        else:
            # unc/smb
            pass
        mount_command.append('./mnt/%s' % share['mm_media_share_guid'])
        logging.debug('mount: %s' % mount_command)
        proc_mnt = subprocess.Popen(mount_command, shell=False)
        proc_mnt.wait()
