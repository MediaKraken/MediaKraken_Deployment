"""
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
"""

# https://github.com/sahlberg/libnfs-python
import libnfs


class CommonNetNFS:
    def __init__(self, hostname, nfs_share):
        self.nfs_inst = libnfs.NFS('nfs://%s/%s' % (hostname, nfs_share))

    def com_net_nfs_writefile(self, file_name, file_data):
        file_handle = self.nfs_inst.open(file_name, mode='w+')
        file_handle.write(file_data)
        file_handle.close()

    def com_net_nfs_readfile(self, file_name):
        return self.nfs_inst.open('/foo-test', mode='r').read()
