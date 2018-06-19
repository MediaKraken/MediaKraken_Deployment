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

from kivy.core.audio import SoundLoader
from plyer import tts

from . import common_global


def com_sound_text_to_speech(message_to_speak):
    """
    # text to speech
    """
    try:
        tts.speak(message_to_speak)
    except NotImplementedError:
        pass


def com_sound_play_file(file_name):
    """
    # play audio file
    """
    try:
        sound_data = SoundLoader.load(file_name)
    except GstPlayerException:
        sound_data = False
    if sound_data:
        common_global.es_inst.com_elastic_index('info', {"Sound found at": sound_data.source})
        common_global.es_inst.com_elastic_index('info', {"Sound is %.3f seconds" %
                                                         sound_data.length})
        sound_data.play()


def com_audio_pyaudio_list_devices():
    """
    # list devices via pyaudio
    """
    import pyaudio
    audio_instance = pyaudio.PyAudio()
    for ndx in range(audio_instance.get_device_count()):
        common_global.es_inst.com_elastic_index('info', {
            'stuff': audio_instance.get_device_info_by_index(ndx))
