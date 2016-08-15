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

# the Roku api docs
# http://sdkdocs.roku.com/display/sdkdoc/External+Control+Guide
from __future__ import absolute_import, division, print_function, unicode_literals
#import logging
import urllib2
import time
import .common_network_ssdp


def mk_roku_network_discovery():
    """
    Discover Roku device(s)
    """
    return common_network_ssdp.SSDP.discover("roku:ecp")


def mk_roku_network_command(roku_addr, roku_port, roku_command, roku_command_seconds):
    """
    Send comment to roku device
    """
    #urllib2.post('http://' + self.roku_address + "/keypress/" + roku_command)
    if roku_command_seconds > 0:
        response = urllib2.urlopen(roku_addr + ':' + roku_port + '/keydown/' + roku_command)
        time.sleep(roku_command_seconds)
        response = urllib2.urlopen(roku_addr + ':' + roku_port + '/keyup/' + roku_command)
    else:
        response = urllib2.urlopen(roku_addr + ':' + roku_port + '/keypress/' + roku_command)
    return response


def mk_roku_network_app_query(roku_addr, roku_port):
    """
    Get list of apps installed
    """
    return urllib2.urlopen(roku_addr + ':' + roku_port + '/query/apps')


def mk_roku_network_app_launch(roku_addr, roku_port, roku_app_id):
    """
    Launch app by id
    """
    return urllib2.urlopen(roku_addr + ':' + roku_port + '/launch/' + roku_app_id)


def mk_roku_network_app_icon(roku_addr, roku_port, roku_app_id):
    """
    Grab app icon
    """
    return urllib2.urlopen(roku_addr + ':' + roku_port + '/query/icon/' + roku_app_id)


def mk_roku_network_touch(roku_addr, roku_port, x, y):
    """
    'Click' screen
    """
    return urllib2.urlopen(roku_addr + ':' + roku_port + '/input?touch.0.x=' + str(x)\
        + '.0&touch.0.y=' + str(y) + '.0&touch.0.op=down')
