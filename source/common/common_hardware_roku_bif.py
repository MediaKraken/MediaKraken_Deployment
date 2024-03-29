#!/bin/env python
"""
Create .bif files for Roku video streaming
Copyright 2009-2013 by Brian C. Lane <bcl@brianlane.com>
All Rights Reserved


Requires ffmpeg to be in the path

NOTE: The jpg image sizes are set to the values posted by bbefilms in the Roku
      development forums. They may or may not be correct for your video aspect ratio.
      They don't look right for me when I set the video height to 480

Modified to use ffprobe: Quinn D Granfor
"""

import array
import json
import os
import shutil
import struct
import subprocess
import tempfile

from common import common_ffmpeg


def getfileinfo(filename):
    """
    Get info about the video
    """
    json_ffmpeg = json.loads(common_ffmpeg.com_ffmpeg_media_attr(filename))
    video_aspect_ratio = float(json_ffmpeg['streams'][0]['width']) / float(
        json_ffmpeg['streams'][0]['height'])
    if video_aspect_ratio > 1.5:
        if float(json_ffmpeg['streams'][0]['height'] >= 720):
            return "320x180", 'HD'  # HD 16:9 ~ 1.7 ratio
        else:
            return "240x136", 'SD'  # SD 16:9 ~ 1.7 ratio
    else:
        if float(json_ffmpeg['streams'][0]['height'] >= 720):
            return "320x240", 'HD'  # HD 4:3 ~ 1.3 ratio
        else:
            return "240x180", 'SD'  # SD 4:3 ~ 1.3 ratio


def extractimages(videofile, directory, interval, resolution, offset=0):
    """
    Extract images from the video at 'interval' seconds

    @param directory Directory to write images into
    @param interval interval to extract images at, in seconds
    @param resolution to create images at
    @param offset offset to first image, in seconds
    """
    proc = subprocess.Popen(["ffmpeg", "-i", videofile,
                             "-ss", "%d" % offset,
                             "-r", "%0.2f" % (1.00 / interval),
                             "-s", resolution,
                             "%s/%%08d.jpg" % directory], stdout=subprocess.PIPE, shell=False)
    (stdout, stderr) = proc.communicate()  # pylint: disable=W0612


def makebif(filename, directory, interval):
    """
    Build a .bif file for the Roku Player Tricks Mode
    @param filename name of .bif file to create
    @param directory Directory of image files 00000001.jpg
    @param interval Time, in seconds, between the images
    """
    images = []
    for image in os.listdir("%s" % directory):
        if image[-4:] == '.jpg':
            images.append(image)
    images.sort()
    images = images[1:]

    file_handle = open(filename, "wb")
    array.array('B', [0x89, 0x42, 0x49, 0x46, 0x0d, 0x0a, 0x1a, 0x0a]).tofile(file_handle)
    file_handle.write(struct.pack("<I1", 0))
    file_handle.write(struct.pack("<I1", len(images)))
    file_handle.write(struct.pack("<I1", 1000 * interval))
    array.array('B', [0x00 for ndx in range(20, 64)]).tofile(file_handle)  # pylint: disable=W0612

    imageindex = 72 + (8 * len(images))  # bif table size
    timestamp = 0

    # Get the length of each image
    for image in images:
        statinfo = os.stat("%s/%s" % (directory, image))
        file_handle.write(struct.pack("<I1", timestamp))
        file_handle.write(struct.pack("<I1", imageindex))

        timestamp += 1
        imageindex += statinfo.st_size

    file_handle.write(struct.pack("<I1", 0xffffffff))
    file_handle.write(struct.pack("<I1", imageindex))

    # Now copy the images
    for image in images:
        data = open("%s/%s" % (directory, image), "rb").read()
        file_handle.write(data)
    file_handle.close()


def com_roku_create_bif(videofile, first_image_offset=7, image_interval=10):
    """
    Create BIF
    """
    # Get info about the video file
    size, res_extension = getfileinfo(videofile)
    tmpdirectory = tempfile.mkdtemp()
    # Extract jpg images from the video file
    extractimages(videofile, tmpdirectory, image_interval,
                  size, first_image_offset)
    biffile = "%s-%s.bif" % (os.path.basename(videofile).rsplit('.', 1)[0], res_extension)
    # Create the BIF file
    makebif(biffile, tmpdirectory, image_interval)
    # Clean up the temporary directory
    shutil.rmtree(tmpdirectory)
