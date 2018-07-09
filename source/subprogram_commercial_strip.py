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

# program will scan for blank images....and auto drop sections < 60 seconds
# ffmpeg -ss 213 -i MySourceMovie.m4v -c:v copy -c:a copy testoutput.m4v
# ffmpeg -ss "00:00:00.000" -i "movie.m4v" -to "00:15:18" -c:v copy -c:a copy "result.pt1.m4v"
# ffmpeg -ss "00:22:29.500" -i "movie.m4v" -to "00:18:58" -c:v copy -c:a copy "result.pt2.m4v"
# ffmpeg -ss "00:50:24.500" -i "movie.m4v" -to "00:16:12" -c:v copy -c:a copy "result.pt3.m4v"
# ffmpeg -ss "01:14:48.500" -i "movie.m4v" -to "00:18:44" -c:v copy -c:a copy "result.pt4.m4v"
# ffmpeg -ss "01:41:35.000" -i "movie.m4v" -to "00:18:08" -c:v copy -c:a copy "result.pt5.m4v"

# ffmpeg -i inputfile.mp4 -vf blackframe=d=0.1:pix_th=.1 -f rawvideo -y /dev/null
# ffmpeg -i test.avi -vf blackdetect=d=1:pic_th=0.70:pix_th=0.10 -an -f null -

# this work?
# ffmpeg -i "$1" -vf blackframe -an -f null - 2>&1 | ack "(?<=frame:)[0-9]*(?= )" -oh > blacks.txt
# ffmpeg -i '/home/spoot/nfsmount/TV_Shows_Misc/Wilfred (2007)/s1e4.avi'
# -vf blackframe -an -f null - 2>&1 | ack "(?<=frame:)[0-9]*(?= )" -oh > blacks.txt
# cat blacks.txt | while read a; do
# printf "not(eq(n\,$a))*"
# done
# rm blacks.txt
# ffmpeg -f concat -i ace-files.txt -c copy ace.tvshow


import getopt
import subprocess
import sys
from shlex import split

from common import common_global
from common import common_logging_elasticsearch


def main(argv):
    """
    Main commercial strip
    """
    # start logging
    common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
        'subprogram_commercial_strip')
    inputfile = None
    outputfile = None
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        common_global.es_inst.com_elastic_index('error', {
            'data': 'subprogram_commercial_strip -i <inputfile> -o <outputfile>'})
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            common_global.es_inst.com_elastic_index('error', {
                'data':
                    'subprogram_commercial_strip -i <inputfile> -o <outputfile>'})
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    # kick off ffmpeg process
    proc = subprocess.Popen(split('./bin/ffmpeg ' + subproccess_args))
    common_global.es_inst.com_elastic_index('info', {"pid": proc.pid,
                                                     "input": inputfile, "output": outputfile})
    proc.wait()


if __name__ == "__main__":
    main(sys.argv[1:])
