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

from __future__ import division
import logging
from PIL import Image


def common_resizeimagecalc(img_size, size):
    """
    Scale image keeping aspect ratio
    """
    picWidth = img_size[0]
    picHeight = img_size[1]
    scaleWidth =  float(size[0] / picWidth)
    scaleHeight = float(size[1] / picHeight)
    if scaleWidth > scaleHeight:
        scale = scaleHeight
    else:
        scale = scaleWidth
    NewWidth = picWidth * scale
    NewHeight = picHeight * scale
    return (NewWidth, NewHeight)


def common_resizeimage(file_name, image_size):
    """
    Resize and save image
    """
    im = Image.open(file_name)
    im.thumbnail(common_resizeimagecalc(im.size, image_size), Image.BICUBIC)
    im.save(file_name + 'thumb', "PNG")
