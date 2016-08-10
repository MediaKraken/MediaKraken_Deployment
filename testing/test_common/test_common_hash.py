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


import pytest
import sys
sys.path.append("../MediaKraken_Common")
from MK_Common_Hash import *


@pytest.mark.parametrize(("file_name", "expected_result"), [
    ('./cache/HashCalc.txt', 'b2dfeef48e0ad8b260674dcf2a8fb92f1456afba'),
    ('./fakedirzz', None)])
def test_MK_Common_Hash_SHA1_By_Filename(file_name, expected_result):
    assert MK_Common_Hash_SHA1_By_Filename(file_name) == expected_result


# c call for sha1 hash
@pytest.mark.parametrize(("file_name", "expected_result"), [
    ('./cache/HashCalc.txt', 'b2dfeef48e0ad8b260674dcf2a8fb92f1456afba'),
    ('./cache/HashCalc.txt.7z', None),
    ('./cache/HashCalc.txt.tar', None),
    ('./cache/HashCalc.txt.tar.bz2', None),
    ('./fakedirzz', None)])
def test_MK_Common_Hash_SHA1_C(file_name, expected_result):
    assert MK_Common_Hash_SHA1_C(file_name) == expected_result


# caclucate crc32 for file
@pytest.mark.parametrize(("file_name", "expected_result"), [
    ('./cache/HashCalc.txt', 'f3c9a423'),
    ('./cache/HashCalc.txt.7z', None),
    ('./cache/HashCalc.txt.tar', None),
    ('./cache/HashCalc.txt.tar.bz2', None),
    ('./fakedirzz', None)])
def test_MK_Common_Hash_CRC32(file_name, expected_result):
    assert MK_Common_Hash_CRC32(file_name) == expected_result


# http://www.radicand.org/blog/orz/2010/2/21/edonkey2000-hash-in-python/
#def MK_Common_Hash_ed2k(filePath):
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
    ("./cache/BigBuckBunny.ogv"),
    ("./cache/BigBuckBunny_512kb.mp4"),
    ("./cache/fake_video.mp4")])
def test_MK_Common_Hash_TheSubDB(file_name):
    MK_Common_Hash_TheSubDB(file_name)


# hash for opensubtiles.org
@pytest.mark.parametrize(("file_name"), [
    ("./cache/BigBuckBunny.ogv"),
    ("./cache/BigBuckBunny_512kb.mp4"),
    ("./cache/fake_video.mp4")])
def test_MK_Common_Hash_OpenSubtitles(file_name)"
    MK_Common_Hash_OpenSubtitles(file_name)
