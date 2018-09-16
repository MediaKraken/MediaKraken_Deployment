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

import ebooklib
# https://github.com/aerkalov/ebooklib/wiki
from ebooklib import epub


class CommonEbookWrite(object):
    """
    Class for interfacing with ebook
    """

    def __init__(self, filename):
        book = epub.read_epub(filename)
        for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
            print(image)


class CommonEbookWrite(object):
    """
    Class for interfacing with ebook
    """

    def __init__(self, filename):
        book = epub.EpubBook()
        # set metadata
        book.set_identifier('id123456')
        book.set_title('Sample book')
        book.set_language('en')

        book.add_author('Author Authorowski')
        book.add_author('Danko Bananko', file_as='Gospodin Danko Bananko', role='ill',
                        uid='coauthor')

        # create chapter
        c1 = epub.EpubHtml(title='Intro', file_name='chap_01.xhtml', lang='hr')
        c1.content = u'<h1>Intro heading</h1><p>Zaba je skocila u baru.</p>'

        # add chapter
        book.add_item(c1)

        # define Table Of Contents
        book.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'),
                    (epub.Section('Simple book'),
                     (c1,))
                    )

        # add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # define CSS style
        style = 'BODY {color: white;}'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css",
                                content=style)

        # add CSS file
        book.add_item(nav_css)

        # basic spine
        book.spine = ['nav', c1]

        # write to the file
        epub.write_epub(filename, book, {})
