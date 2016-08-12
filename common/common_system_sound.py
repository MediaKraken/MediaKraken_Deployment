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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from plyer import tts
from kivy.core.audio import SoundLoader


# text to speech
def MK_Sound_Text_To_Speech(message_to_speak):
    tts.speak(message_to_speak)


# play audio file
def MK_Sound_Play_File(file_name):
    sound_data = SoundLoader.load(file_name)
    if sound_data:
        logging.debug("Sound found at %s" % sound_data.source)
        logging.debug("Sound is %.3f seconds" % sound_data.length)
        sound_data.play()


# list devices via pyaudio
def com_Audio_Pyaudio_List_Devices():
    import pyaudio
    audio_instance = pyaudio.PyAudio()
    for ndx in range(audio_instance.get_device_count()):
        logging.info(audio_instance.get_device_info_by_index(ndx))
