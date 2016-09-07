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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import subprocess
import sys
import getopt
from common import common_logging


def main(argv):
    """
    Launch ffmpeg process
    """
    # start logging
    common_logging.com_logging_start('./log/MediaKraken_Subprogram_Cron')
    inputfile = None
    outputfile = None
    vid_codec = []
    quality_arg = []
    audio_codec = []
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        logging.debug('subprogram_ffmpeg_process.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            logging.debug('subprogram_ffmpeg_process.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    subproccess_args = []
    subproccess_args.extend(('-i', inputfile))
    subproccess_args.extend(vid_codec)
    subproccess_args.extend(quality_arg)
    subproccess_args.extend(audio_codec)
    subproccess_args.extend(('-o', outputfile))
    # kick off ffmpeg process
    proc = subprocess.Popen(['ffmpeg', subproccess_args], shell=False)
    logging.debug("FFMpeg PID %s:", proc.pid)
    proc.wait()


if __name__ == "__main__":
    main(sys.argv[1:])
