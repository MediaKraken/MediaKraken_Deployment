"""
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
"""

# import modules
import base64
import os

fin = open("ImageData.txt", "w")
fin.write("embed_image_data = {")
# insert the path to the directory of interest
path = "../images_to_embed/flags"
dirList = os.listdir(path)
for fname in dirList:
    iconfile = open(path + "/" + fname, "rb")
    fin.write("\"flag_" + fname.split(".")[0] + "\": \""
        + base64.b64encode(iconfile.read()) + "\",")
    iconfile.close()
path = "./images_to_embed/os"  # insert the path to the directory of interest
dirList = os.listdir(path)
for fname in dirList:
    iconfile = open(path + "/" + fname, "rb")
    fin.write("\"os_" + fname.split(".")[0] + "\": \""
              + base64.b64encode(iconfile.read()) + "\",")
    iconfile.close()
# insert the path to the directory of interest
path = "../images_to_embed/systems_controllers_media"
dirList = os.listdir(path)
for fname in dirList:
    iconfile = open(path + "/" + fname, "rb")
    fin.write("\"controller_" + fname.split(".")[0] + "\": \""
              + base64.b64encode(iconfile.read()) + "\",")
    iconfile.close()
fin.write("}")
fin.close()
