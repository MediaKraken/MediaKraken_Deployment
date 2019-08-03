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

import os

import pytest  # pylint: disable=W0611
from selenium import webdriver

TEST_TARGET = 'https://th-mediakraken-1:8900'

browsers = {
    'chrome': webdriver.Chrome,
    # webdriver.ChromeOptions
    # 'firefox': webdriver.Firefox,
    # webdriver.FirefoxProfile
    # 'ie': webdriver.Ie,
    # 'Opera': webdriver.Opera,
    # 'PhantomJS': webdriver.PhantomJS,
    # webdriver.Remote
    # webdriver.DesiredCapabilities
    # webdriver.ActionChains
    # webdriver.TouchActions
    # webdriver.Proxy
}


@pytest.fixture(scope='session', params=browsers.keys())
def driver(request):
    """
    Determine if webdriver exists
    """
    if 'DISPLAY' not in os.environ:
        pytest.skip('Test requires display server')
    b = browsers[request.param]()
    request.addfinalizer(lambda *args: b.quit())
    return b
