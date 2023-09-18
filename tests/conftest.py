import os

import pytest
from flask import render_template
from selenium import webdriver
from flask_fixture import endpoint, config


@config
class MyConfig:
    port: int = 5001
    template_folder: str = os.path.join(
        'tests',
        'integrations',
        'templates',
    )


@endpoint('/')
def root():
    return render_template('index.html')


@pytest.fixture(scope='session')
def chrome_options():
    """
    Фикстура для установки различных опций для веб-драйвера.
    Возвращает объект Options.
    """
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    return options


@pytest.fixture(scope='session')
def driver(chrome_options):
    """
    Фикстура для создания веб-драйвера с необходимыми опциями.
    Вовзращает объект WebDriver.
    """
    one_driver = webdriver.Chrome(chrome_options)
    return one_driver

