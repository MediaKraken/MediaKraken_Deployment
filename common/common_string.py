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

import logging
import re
import passwordmeter
from socket import inet_ntoa


def repl_func(m):
    """process regular expression match groups for word upper-casing problem"""
    return m.group(1) + m.group(2).upper()


# def capitalize first letter of each word and handling quotes
def MK_Common_String_Title(title_string):
    return re.sub("(^|\s)(\S)", repl_func, title_string)


# readable numbers for bytes to G, T, etc
def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    if n == 0 or type(n) == str:
        return '0B'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


# test password
def MK_Common_String_Password_Test(password_text):
    ratings = (
      'Infinitely weak',
      'Extremely weak',
      'Very weak',
      'Weak',
      'Moderately strong',
      'Strong',
      'Very strong',
    )
    strength, improvements = passwordmeter.test(password_text)
    logging.info('Password strength: {} ({})'.format(strength, (ratings[min(len(ratings) - 1, int(strength * len(ratings)))])))
    return (strength, improvements)


def ip_ascii_to_int(ip):
    octets = [int(octet) for octet in ip.split('.')]
    if len(octets) != 4:
        raise Exception("IP [%s] does not have four octets." % (ip))
    encoded = ("%02x%02x%02x%02x" % (octets[0], octets[1], octets[2], octets[3]))
    return int(encoded, 16)


def ip_int_to_ascii(ip_int):
    return inet_ntoa(hex(ip_int)[2:-1].zfill(8).decode('hex'))


# break up unc to parts
def UNC_To_Addr_Share_Path(unc_path):
    return (unc_path.split('\\', 5)[2], unc_path.split('\\', 5)[3], '\\'.join(unc_path.split('\\', 5)[4:]))
