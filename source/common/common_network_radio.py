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

import subprocess
import sys

sys.path.append("./common/radio_crawler")
from . import common_global


def com_net_radio():
    """
    # create the cache file for import
    """
    proc = subprocess.Popen(['python3', '../MediaKraken_Common/radio_crawler/crawler_google.py'],
                            stdout=subprocess.PIPE, shell=False)
    common_global.es_inst.com_elastic_index('info', {"Crawler Google PID": proc.pid})
    proc.wait()

    proc = subprocess.Popen(['python3', '../MediaKraken_Common/radio_crawler/clean_uris.py'],
                            stdout=subprocess.PIPE, shell=False)
    common_global.es_inst.com_elastic_index('info', {"Clean Uris PID": proc.pid})
    proc.wait()

    proc = subprocess.Popen(['python3', '../MediaKraken_Common/radio_crawler/init_cache.py'],
                            stdout=subprocess.PIPE, shell=False)
    common_global.es_inst.com_elastic_index('info', {"Init Cache PID": proc.pid})
    proc.wait()

    proc = subprocess.Popen(['python3', '../MediaKraken_Common/radio_crawler/fetch_xiph.py'],
                            stdout=subprocess.PIPE, shell=False)
    common_global.es_inst.com_elastic_index('info', {"Fetch Xiph PID": proc.pid})
    proc.wait()

    proc = subprocess.Popen(['python3', '../MediaKraken_Common/radio_crawler/fetch_tags.py'],
                            stdout=subprocess.PIPE, shell=False)
    common_global.es_inst.com_elastic_index('info', {"Fetch Tags PID": proc.pid})
    proc.wait()

    proc = subprocess.Popen(['python3', '../MediaKraken_Common/radio_crawler/fetch_cast.py'],
                            stdout=subprocess.PIPE, shell=False)
    common_global.es_inst.com_elastic_index('info', {"Fetch Cast PID": proc.pid})
    proc.wait()

    proc = subprocess.Popen(['python3', '../MediaKraken_Common/radio_crawler/fetch_tags.py'],
                            stdout=subprocess.PIPE, shell=False)
    common_global.es_inst.com_elastic_index('info', {"Fetch Tags PID": proc.pid})
    proc.wait()

    proc = subprocess.Popen(['python3', '../MediaKraken_Common/radio_crawler/dump_taglist.py'],
                            stdout=subprocess.PIPE, shell=False)
    common_global.es_inst.com_elastic_index('info', {"Dump Taglist PID": proc.pid})
    proc.wait()
