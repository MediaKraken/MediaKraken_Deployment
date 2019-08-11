"""
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

import isbnlib


# https://github.com/MediaKraken-Dependancies/isbnlib

def com_isbn_10_check(isbn_string):
    return isbnlib.is_isbn10(isbn_string)


def com_isbn_13_check(isbn_string):
    return isbnlib.is_isbn13(isbn_string)


def com_isbn_13_to_10(isbn_string):
    return isbnlib.to_isbn10(isbn_string)


def com_isbn_10_to_13(isbn_string):
    return isbnlib.to_isbn13(isbn_string)


def com_isbn_info(isbn_string):
    """
    Get the language or country assigned to this isbn
    """
    return isbnlib.info(isbn_string)


def com_isbn_cover(isbn_string):
    """
    Returns a dictionary with the url for cover.Almost all data available are for US books!
    """
    return isbnlib.cover(isbn_string)


def com_isbn_mask(isbn_string, isbn_seperator='-'):
    """
    Mask (hyphenate) a canonical ISBN.
    """
    return isbnlib.mask(isbn_string, separator=isbn_seperator)


def com_isbn_meta(isbn_string):
    """
    Gives you the main metadata associated with the ISBN. As service parameter you can use: 'goob' uses the Google Books service (no key is needed) and is the default option, 'openl' uses the OpenLibrary.org api (no key is needed). You can enter API keys with config.add_apikey(service, apikey) (see example below). The output can be formatted as bibtex, csl (CSL-JSON), msword, endnote, refworks, opf or json (BibJSON) bibliographic formats with isbnlib.registry.bibformatters. cache only allows two values: 'default' or None. You can change the kind of cache by using isbnlib.registry.set_cache (see below). Now, you can extend the functionality of this function by adding pluggins, more metadata providers or new bibliographic formatters (check for available pluggins).
    """
    return isbnlib.meta(isbn_string, service='default', cache='default')


def com_isbn_editions(isbn_string):
    """
    Returns the list of ISBNs of editions related with this ISBN. By default uses 'merge' (merges 'openl' and 'thingl'), but other providers are available: 'openl' users Open Library, 'thingl' (uses the service ThingISBN from LibraryThing) and 'any' (first tries 'openl', if no data, then 'thingl').
    """
    return isbnlib.editions(isbn_string, service='merge')


def com_isbn_lookup_title(title_words):
    """
    Returns the most probable ISBN from a list of words (for your geographic area).
    """
    return isbnlib.isbn_from_words(title_words)


def com_isbn_google_search(title_words):
    """
    Returns a list of references from Google Books multiple references.
    """
    return isbnlib.goom(title_words)


def com_isbn_rename_file(file_name):
    """
    Renames a file using metadata from an ISBN in his filename.
    """
    return isbnlib.ren(file_name)


def com_isbn_description(isbn_string):
    """
    Returns a small description of the book. Almost all data available are for US books!
    """
    return isbnlib.desc(isbn_string)
