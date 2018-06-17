'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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

import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
from common import common_hash


@pytest.mark.parametrize(("file_name", "expected_result"), [
    ('./testing/cache/HashCalc.txt', 'b2dfeef48e0ad8b260674dcf2a8fb92f1456afba'),
    ('./testing/fakedirzz', None)])
def test_com_hash_sha1_by_filename(file_name, expected_result):
    """
    Test function
    """
    assert common_hash.com_hash_sha1_by_filename(file_name) == expected_result


# c call for sha1 hash
@pytest.mark.parametrize(("file_name", "expected_result"), [
    ('./testing/cache/HashCalc.txt', 'b2dfeef48e0ad8b260674dcf2a8fb92f1456afba'),
    ('./testing/cache/HashCalc.txt.7z', '8424944223b7437d9f5c33459b97a58961a726a7'),
    ('./testing/cache/HashCalc.txt.tar', '22b1b418d3822997b4c80e7fcf3394ebd7e1bdbe'),
    ('./testing/cache/HashCalc.txt.tar.bz2',
     '7c9f83432b09e2607995ebf050c734fb347659b0'),
    ('./testing/fakedirzz', None)])
def test_com_hash_sha1_c(file_name, expected_result):
    """
    Test function
    """
    assert common_hash.com_hash_sha1_c(file_name) == expected_result


# caclucate crc32 for file
@pytest.mark.parametrize(("file_name", "expected_result"), [
    ('./testing/cache/HashCalc.txt', 'f3c9a423'),
    ('./testing/cache/HashCalc.txt.7z', '2269317160'),
    ('./testing/cache/HashCalc.txt.tar', '1490977407'),
    ('./testing/cache/HashCalc.txt.tar.bz2', '3098236506'),
    ('./testing/fakedirzz', None)])
def test_com_hash_crc32(file_name, expected_result):
    """
    Test function
    """
    assert common_hash.com_hash_crc32(file_name) == expected_result


# http://www.radicand.org/blog/orz/2010/2/21/edonkey2000-hash-in-python/
# def com_hash_ed2k(filePath):
#    """ Returns the ed2k hash of a given file."""
#    md4 = hashlib.new('md4').copy
#    def gen(f):
#        while True:
#            x = f.read(9728000)
#            if x: yield x
#            else: return
#
#    def md4_hash(data):
#        m = md4()
#        m.update(data)
#        return m
#
#    with open(filePath, 'rb') as f:
#        a = gen(f)
#        hashes = [md4_hash(data).digest() for data in a]
#        if len(hashes) == 1:
#            return hashes[0].encode("hex")
#        else: return md4_hash(reduce(lambda a,d: a + d, hashes, "")).hexdigest()


# hash for thesubdb
@pytest.mark.parametrize(("file_name"), [
    ("./testing/cache/BigBuckBunny.ogv"),
    ("./testing/cache/BigBuckBunny_512kb.mp4"),
    ("./testing/cache/fake_video.mp4")])
def test_com_hash_thesubdb(file_name):
    """
    Test function
    """
    common_hash.com_hash_thesubdb(file_name)


# hash for opensubtiles.org
@pytest.mark.parametrize(("file_name"), [
    ("./testing/cache/BigBuckBunny.ogv"),
    ("./testing/cache/BigBuckBunny_512kb.mp4"),
    ("./testing/cache/fake_video.mp4")])
def test_com_hash_opensubtitles(file_name):
    """
    Test function
    """
    common_hash.com_hash_opensubtitles(file_name)
