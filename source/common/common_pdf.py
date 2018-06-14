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

import pdfkit


def com_pdf_create(pdf_from, pdf_data, pdf_out_file):
    if pdf_from == 'url':
        pdfkit.from_url(pdf_data, pdf_out_file)
    elif pdf_from == 'file':
        pdfkit.from_file(pdf_data, pdf_out_file)
    else:
        pdfkit.from_string(pdf_data, pdf_out_file)
