import os

import pytest
from selenium import webdriver
from flask_fixture import endpoint


with open(os.path.join(os.getcwd(), 'templates/index.html'), "r", encoding='utf-8') as page:
    index_html = page.read()


@endpoint('/')
def root():
    return index_html


@pytest.fixture(scope='session')
def chrome_options():
    """
    Фикстура для установки различных опций для веб-драйвера.
    Возвращает объект Options.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    return options


@pytest.fixture(scope='session')
def driver(chrome_options):
    """
    Фикстура для создания веб-драйвера с необходимыми опциями.
    Вовзращает объект WebDriver.
    """
    one_driver = webdriver.Chrome(chrome_options)
    return one_driver

