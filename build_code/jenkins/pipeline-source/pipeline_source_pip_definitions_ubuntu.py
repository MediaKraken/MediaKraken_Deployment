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
import sys
sys.path.append('.')
sys.path.append('../MediaKraken-PyLint') # for jenkins server

PIP_UBUNTU_1604 = [
    'service_identity',
    'psutil',
    'requests>=2.11.1',
    'psycopg2',
    'pyOpenSSL',
    'tmdbsimple',
    'plyer',
    'dropbox',
    'boto',
    'pylzma',
    'pytvmaze',
    'musicbrainzngs',
    'watchdog',
    'onedrivesdk',
    'fastnumbers',
    'natsort',
    'xmltodict',
    'google-api-python-client',
    'Flask',
    'Flask-WeasyPrint',
    'Flask-Login',
    'Flask-Cache',
    'Flask-Bcrypt',
    'Flask-WTF',
    'Flask-Babel',
    'Flask-Mail',
    'Flask-Openid',
    'Flask-Paginate',
    'Flask-Moment',
    'Flask-Assets',
    'Flask-SQLAlchemy',
    'Flask-Migrate',
    'Flask-KVSession',
    'ipgetter',
    'pytvdbapi',
    'fuzzywuzzy',
    'youtube_dl',
    'subliminal',
    'httplib2',
    'oauth2client',
    'python-nest',
    'uritemplate',
    'feedgen',
    'imdbpie',
    'nest',
    'twisted',
    'easysnmp',
    'trakt',
    'transmissionrpc',
    'steam',
    'guessit',
    'passwordmeter',
    'beautifulsoup4',
    'klein',
    'futures',
    'pysmb',
    'scandir',
    'flask-uploads',
    'synolopy',
    'pychromecast',
    'PyVimeo',
    'pitchfork',
    'pygal',
    'flickrapi',
    'rxv',
    'python-twitch',
    'pillow',
    'python-ldap',
    'omdb',
    'pyaudio',
    'onkyo-eiscp',
    'pycrypto',
    'Adafruit_BBIO',
    'arduino-python',
    'NetflixRouletteAPI',
    'python-libdiscid',
    ]