"""
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
"""

# https://github.com/MediaKraken-Dependancies/packtpub-library-downloader


"""
Usage:
python downloader.py -e <email> -p <password> [-d <directory> -b <book assets> -v <video assets>]

Example: Download books in PDF and EPUB formats and accompanying source code
python downloader.py -e hello@world.com -p p@ssw0rd -d ~/Desktop/packt -b pdf,epub,code

Example: Download videos, their cover image, and accompanying source code
python downloader.py -e hello@world.com -p p@ssw0rd -d ~/Desktop/packt -v video,cover,code

Example: Download Integrated Courses (Interactive-Ebooks), their cover image, and accompanying source code
python downloader.py -e hello@world.com -p p@ssw0rd -d ~/Desktop/packt -c course,cover,code

Example: Download everything
python downloader.py -e hello@world.com -p p@ssw0rd -d ~/Desktop/packt -b pdf,epub,mobi,cover,code,info -v video,cover,code -c course,cover,code
"""
