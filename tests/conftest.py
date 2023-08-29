import multiprocessing
from flask_app import run_flask

import pytest
from selenium import webdriver


@pytest.fixture(scope='session')
def chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    return options


@pytest.fixture(scope='session')
def driver(chrome_options):
    one_driver = webdriver.Chrome(chrome_options)
    return one_driver


@pytest.fixture(scope='session')
def url():
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=run_flask, args=(queue, ))
    process.start()
    queue.get()
    yield 'http://127.0.0.1:8000'
    process.terminate()

