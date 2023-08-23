import multiprocessing
import time
from base_page.tests.flask_app.app import run_flask

import pytest
from selenium import webdriver


@pytest.fixture()
def chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    return options


@pytest.fixture()
def driver(chrome_options):
    one_driver = webdriver.Chrome(chrome_options)
    return one_driver


@pytest.fixture(scope='session')
def url():
    process = multiprocessing.Process(target=run_flask, args=())
    process.start()
    time.sleep(0.5)
    yield 'http://127.0.0.1:8000'
    process.terminate()
