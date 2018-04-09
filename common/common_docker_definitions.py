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

from __future__ import absolute_import, division, print_function, unicode_literals

import os

DOCKER_ELK = ()

DOCKER_MUMBLE = ()

DOCKER_MUSICBRAINZ = ()

DOCKER_PORTAINER = ()

DOCKER_PGADMIN = ()

DOCKER_SMTP = ()

DOCKER_TEAMSPEAK = ()

DOCKER_TRANSMISSION = ('/start-transmission.sh', 'mktransmission',
                       'mediakraken/mktransmission', True,
                       {"9091": 9091, "51413/tcp": 51413, "51413/udp": 51413},
                       'mk_mediakraken_network',
                       ['/var/opt/mediakraken/transmission/downloads:/transmission/downloads',
                        '/var/opt/mediakraken/transmission/incomplete:/transmission/incomplete'],
                       True,
                       {'USERNAME': os.environ['TRANSUSER'],
                        'PASSWORD': os.environ['TRANSPASSWORD']}
                       )
