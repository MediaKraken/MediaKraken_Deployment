from distutils.core import setup

setup(
    name = 'isbn_hyphenate',
    packages = ['isbn_hyphenate', 'isbn_hyphenate.test'],
    version = '1.0.4',
    description = 'a Python library to add hyphens in the right place to an ISBN (International Standard Book Number)',
    author = 'Tor Klingberg',
    author_email = 'tor.klingberg@gmail.com',
    url = 'https://github.com/TorKlingberg/isbn_hyphenate',
    license = "LGPL",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: General',
        'Topic :: Printing',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
