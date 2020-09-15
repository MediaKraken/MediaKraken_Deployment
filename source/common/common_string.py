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

import re
from socket import inet_ntoa

from common import common_logging_elasticsearch_httpx

STACK_CD = re.compile('-cd\d', re.IGNORECASE)
STACK_CD1 = re.compile('-cd1(?!\d)', re.IGNORECASE)
STACK_PART = re.compile('-part\d', re.IGNORECASE)
STACK_PART1 = re.compile('-part1(?!\d)', re.IGNORECASE)
STACK_DVD = re.compile('-dvd\d', re.IGNORECASE)
STACK_DVD1 = re.compile('-dvd1(?!\d)', re.IGNORECASE)
STACK_PT = re.compile('-pt\d', re.IGNORECASE)
STACK_PT1 = re.compile('-pt1(?!\d)', re.IGNORECASE)
STACK_DISK = re.compile('-disk\d', re.IGNORECASE)
STACK_DISK1 = re.compile('-disk1(?!\d)', re.IGNORECASE)
STACK_DISC = re.compile('-disc\d', re.IGNORECASE)
STACK_DISC1 = re.compile('-disc1(?!\d)', re.IGNORECASE)


def com_string_repl_func(m):
    """process regular expression match groups for word upper-casing problem"""
    return m.group(1) + m.group(2).upper()


def com_string_title(title_string):
    """
    capitalize first letter of each word and handling quotes
    """
    from titlecase import titlecase
    return titlecase(title_string)


def com_string_bytes2human(num_bytes):
    """
    Readable numbers for bytes to G, T, etc
    """
    # http://code.activestate.com/recipes/578019
    if num_bytes == 0 or type(num_bytes) == str:
        return '0B'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for ndx in reversed(symbols):
        if num_bytes >= prefix[ndx]:
            value = float(num_bytes) / prefix[ndx]
            return '%.1f%s' % (value, ndx)
    return "%sB" % num_bytes


def com_string_password_test(password_text):
    """
    Test password strength
    """
    import passwordmeter
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
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
        'Password strength: {} ({})'.format(
            strength, (ratings[min(len(ratings) - 1, int(strength * len(ratings)))]))})
    return (strength, improvements)


def com_string_ip_ascii_to_int(ip_addr):
    """
    Return int from ascii IP
    """
    octets = [int(octet) for octet in ip_addr.split('.')]
    if len(octets) != 4:
        raise Exception("IP [%s] does not have four octets." % (ip_addr))
    encoded = ("%02x%02x%02x%02x" %
               (octets[0], octets[1], octets[2], octets[3]))
    return int(encoded, 16)


def com_string_ip_int_to_ascii(ip_int):
    """
    Return ascii from IP integer
    """
    return inet_ntoa(hex(ip_int)[2:-1].zfill(8).decode('hex'))


def com_string_unc_to_addr_path(unc_path):
    """
    Break up unc to parts
    """
    try:
        return (unc_path.split('\\', 5)[2], unc_path.split('\\', 5)[3],
                '\\'.join(unc_path.split('\\', 5)[4:]))
    except:
        return None, None, None


def com_string_guessit_list(guessit_list):
    """
    combine guessing lists
    """
    return_string = ''
    for title_name in guessit_list:
        return_string += title_name + ' '
    return return_string.strip()


def com_string_escape_file_path(file_path):
    return file_path.translate(str.maketrans({" ": r"\ ", "'": r"\'"}))
