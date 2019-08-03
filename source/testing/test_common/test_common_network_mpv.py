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

import sys

sys.path.append('.')
# from common import common_network_mpv
#
# mpv_pid = subprocess.Popen(split('mpv --hwdec=auto --input-ipc-server ./mk_mpv.sock \"' +
#                             '/home/spoot/mnt/HTPC_MediaBrowser/BluRay_Dir_Cut/Underworld (2003)/Underworld (2003).mkv' + '\"'))
# # mpv_ipc = common_network_mpv.CommonNetMPV()
# mpv_ipc = common_network_mpv.CommonNetMPVSocat()
# time.sleep(5)
# mpv_ipc.execute('{"command": ["get_property", "playback-time"]}')
# time.sleep(5)
# mpv_ipc.execute('{"command": ["set_property", "pause", true]}')
# time.sleep(5)
# mpv_ipc.execute('{"command": ["quit"]})')
# mpv_ipc.close()
