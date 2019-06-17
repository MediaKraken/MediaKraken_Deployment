'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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

import pycountry
from babel.dates import format_date
from babel.numbers import format_decimal


def com_inter_date_format(date_to_format, country_code='en_US'):
    return format_date(date_to_format, locale=country_code)


def com_inter_number_format(number_to_format, country_code='en_US'):
    return format_decimal(number_to_format, locale=country_code)


def com_inter_country_name(country_code='eng'):
    try:
        lang = pycountry.languages.get(alpha_3=country_code)
    except KeyError:
        return country_code
    if lang is None:
        return country_code
    return lang.name
