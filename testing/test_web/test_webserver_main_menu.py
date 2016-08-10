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
from test_webserver_base import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def test_main_index(driver):
    driver.get(TEST_TARGET)
    assert 'MediaKraken' in driver.title


def test_main_login(driver):
    driver.get(TEST_TARGET)
    driver.find_element_by_id('main_username').send_keys('metaman')
    driver.find_element_by_id('main_password').send_keys('metaman')
    driver.find_element_by_id('main_button_login').click()
    

def test_main_menu_metaman(driver):
    driver.get(TEST_TARGET)
    driver.find_element_by_id('menu_home').click()
    assert 'MediaKraken' in driver.title


def test_main_menu_media(driver):
    driver.get(TEST_TARGET)
    driver.find_element_by_id('menu_media').click()
    assert 'MediaKraken' in driver.title


def test_main_menu_sync(driver):
    driver.get(TEST_TARGET)
    driver.find_element_by_id('menu_sync').click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_movies(driver):
    driver.get(TEST_TARGET)  
    hov = ActionChains(driver).move_to_element(driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu_metadata_movies")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_movie_collection(driver):
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu_metadata_movie_collection")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_tv_shows(driver):
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(driver.find_element_by_id('menu_metadata'))
    hov.perform()   
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu_metadata_tv_shows")))
    element.click()    
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_music(driver):
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu_metadata_music")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_music_albums(driver):
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu_metadata_music_albums")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_music_videos(driver):
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu_metadata_music_videos")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_sports(driver):
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu_metadata_sports")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_games(driver):
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu_metadata_games")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_game_systems(driver):
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu_metadata_game_systems")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_people(driver):
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu_metadata_people")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_metadata_class_list(driver):
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "menu_metadata_class_list")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_server(driver):
    driver.get(TEST_TARGET)
    driver.find_element_by_id('menu_server').click()
    assert 'MediaKraken' in driver.title


def test_main_menu_about(driver):
    driver.get(TEST_TARGET)
    driver.find_element_by_id('menu_about').click()
    assert 'MediaKraken' in driver.title


def test_main_menu_contact(driver):
    driver.get(TEST_TARGET)
    driver.find_element_by_link_text('Contact').click()
