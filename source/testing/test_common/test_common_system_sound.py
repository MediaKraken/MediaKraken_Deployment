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
from common import common_system_sound


# text to speech
@pytest.mark.parametrize(("message_to_speak"), [
    ("first test"),
    ("can you hear me again")])
def test_com_sound_text_to_speech(message_to_speak):
    """
    Test function
    """
    common_system_sound.com_sound_text_to_speech(message_to_speak)


# play audio file
@pytest.mark.parametrize(("file_name"), [
    ("./testing/cache/250Hz_44100Hz_16bit_05sec.wav"),
    ("./testing/cache/250Hz_44100Hz_16bit_05sec.mp3")])
def test_com_sound_play_file(file_name):
    """
    Test function
    """
    common_system_sound.com_sound_play_file(file_name)


# list devices via pyaudio
def test_com_audio_pyaudio_list_devices():
    """
    Test function
    """
    common_system_sound.com_audio_pyaudio_list_devices()
