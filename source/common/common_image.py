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

from PIL import Image


def com_image_resizeimagecalc(img_size, size):
    """
    Scale image keeping aspect ratio
    """
    picwidth = img_size[0]
    picheight = img_size[1]
    scalewidth = float(size[0] / picwidth)
    scaleheight = float(size[1] / picheight)
    if scalewidth > scaleheight:
        scale = scaleheight
    else:
        scale = scalewidth
    return (picwidth * scale, picheight * scale)


def com_image_resizeimage(file_name, image_size):
    """
    Resize and save image
    """
    im_data = Image.open(file_name)
    im_data.thumbnail(com_image_resizeimagecalc(
        im_data.size, image_size), Image.BICUBIC)
    im_data.save(file_name + 'thumb', "PNG")
