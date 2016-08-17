'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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

# import modules
import sys

__version_info__ = (0, 0, 6)
__version__ = '.'.join(map(str, __version_info__))

# verify twisted is installed and available to the server
try:
    from twisted import version as twisted_version
    from twisted.web import version as twisted_web_version
    from twisted.python.versions import Version
except ImportError, exc:
    sys.stderr.write("Twisted >= 14.0.2 is required.\n")
    raise

# verify the version numbers for twisted
try:
    if twisted_version < Version("twisted", 14, 0, 2):
        raise ImportError("Twisted 14.0.2 or higher is required.")
    if twisted_web_version < Version("twisted", 14, 0, 2):
        raise ImportError("Twisted version 14.0.2 or higher is required.")
except ImportError, exc:
    for arg in exc.args:
        sys.stderr.write("%s\n" % arg)
    raise
