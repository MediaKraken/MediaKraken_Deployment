#!/bin/env python
"""
Create .bif files for Roku video streaming
Copyright 2009-2013 by Brian C. Lane <bcl@brianlane.com>
All Rights Reserved


makebif.py --help for arguments

Requires ffmpeg to be in the path

NOTE: The jpg image sizes are set to the values posted by bbefilms in the Roku
      development forums. They may or may not be correct for your video aspect ratio.
      They don't look right for me when I set the video height to 480
"""

import array
import os
import shutil
import struct
import tempfile
from subprocess import Popen, PIPE

# for mode 0, 1, 2, 3
VIDEOSIZES = [(240, 180), (320, 240), (240, 136), (320, 180)]

# Extension to add to the file for mode 0, 1, 2, 3
MODEEXTENSION = ['SD', 'HD', 'SD', 'HD']


def getmp4info(filename):
    """
    Get mp4 info about the video
    """
    details = {'type': "", 'length': 0,
               'bitrate': 1500, 'format': "", 'size': ""}
    cmd = ["mp4info", filename]
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    (stdout, stderr) = proc.communicate()  # pylint: disable=W0612
    # Parse the results
    for line in stdout.split('\n'):
        fields = line.split(None, 2)
        try:
            if fields[1] == 'video':
                # parse the video info
                # MPEG-4 Simple @ L3, 5706.117 secs, 897 kbps, 712x480 @ 23.9760 24 fps
                videofields = fields[2].split(',')
                details['type'] = videofields[0]
                details['length'] = float(videofields[1].split()[0])
                details['bitrate'] = float(videofields[2].split()[0])
                details['format'] = videofields[3]
                details['size'] = videofields[3].split('@')[0].strip()
        except:
            pass
    return details


def extractimages(videofile, directory, interval, mode=0, offset=0):
    """
    Extract images from the video at 'interval' seconds

    @param mode 0=SD 4:3 1=HD 4:3 2=SD 16:9 3=HD 16:9
    @param directory Directory to write images into
    @param interval interval to extract images at, in seconds
    @param offset offset to first image, in seconds
    """
    size = "x".join([str(ndx) for ndx in VIDEOSIZES[mode]])
    cmd = ["ffmpeg", "-i", videofile, "-ss", "%d" % offset,
           "-r", "%0.2f" % (1.00 / interval), "-s", size, "%s/%%08d.jpg" % directory]
    proc = Popen(cmd, stdout=PIPE, stdin=PIPE)
    (stdout, stderr) = proc.communicate()  # pylint: disable=W0612


def makebif(filename, directory, interval):
    """
    Build a .bif file for the Roku Player Tricks Mode
    @param filename name of .bif file to create
    @param directory Directory of image files 00000001.jpg
    @param interval Time, in seconds, between the images
    """
    magic = [0x89, 0x42, 0x49, 0x46, 0x0d, 0x0a, 0x1a, 0x0a]
    version = 0

    files = os.listdir("%s" % (directory))
    images = []
    for image in files:
        if image[-4:] == '.jpg':
            images.append(image)
    images.sort()
    images = images[1:]

    file_handle = open(filename, "wb")
    array.array('B', magic).tofile(file_handle)
    file_handle.write(struct.pack("<I1", version))
    file_handle.write(struct.pack("<I1", len(images)))
    file_handle.write(struct.pack("<I1", 1000 * interval))
    array.array('B', [0x00 for ndx in range(20, 64)]).tofile(
        file_handle)  # pylint: disable=W0612

    biftablesize = 8 + (8 * len(images))
    imageindex = 64 + biftablesize
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


def com_roku_create_bif(videofile, first_image_offset=7, image_interval=10, option_mode=0):
    """
    Create BIF
    """
    # help="(0=SD) 4:3 1=HD 4:3 2=SD 16:9 3=HD 16:9") - option_mode
    # Get info about the video file
    videoinfo = getmp4info(videofile)
    if videoinfo["size"]:
        size = videoinfo["size"].split("x")
        aspectratio = float(size[0]) / float(size[1])
        width, height = VIDEOSIZES[option_mode]
        height = int(width / aspectratio)
        VIDEOSIZES[option_mode] = (width, height)
    tmpdirectory = tempfile.mkdtemp()
    # Extract jpg images from the video file
    extractimages(videofile, tmpdirectory, image_interval,
                  option_mode, first_image_offset)
    biffile = "%s-%s.bif" % (os.path.basename(videofile).rsplit('.', 1)[0],
                             MODEEXTENSION[option_mode])
    # Create the BIF file
    makebif(biffile, tmpdirectory, image_interval)
    # Clean up the temporary directory
    shutil.rmtree(tmpdirectory)
