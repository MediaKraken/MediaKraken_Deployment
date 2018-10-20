'''
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
'''

# https://github.com/MediaKraken-Dependancies/speech_recognition
# pip install SpeechRecognition

import speech_recognition as sr


class CommonSpeechRec(object):
    """
    Class for interfacing with speech recording/etc
    """

    def __init__(self):
        self.audio = None
        self.recognizer = None

    def com_speech_record(self):
        # obtain audio from the microphone
        self.recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.audio = self.recognizer.listen(source)

    def com_speech_from_file(self, file_name):
        # use the audio file as the audio source
        self.recognizer = sr.Recognizer()
        with sr.AudioFile(file_name) as source:
            self.audio = self.recognizer.record(source)

    def com_decode_audio(self):
        try:
            print("Sphinx thinks you said " + self.recognizer.recognize_sphinx(self.audio))
            return self.recognizer.recognize_sphinx(self.audio)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
            return None
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
            return None
