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

from googletrans import Translator


class CommonMetadataTranslator(object):
    """
    Class for interfacing with google translator
    """

    def __init__(self, db_connection):
        self.translator = Translator()

    def com_meta_translator(self, trans_text, lang_code='en'):
        # TODO will need to handle stuff > 15k characters at once
        return self.translator.translate(trans_text, dest=lang_code)
