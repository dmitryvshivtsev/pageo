import multiprocessing
import time
from core_page.tests.flask_app.app import run_flask

import pytest


@pytest.fixture(scope='session')
def url():
    process = multiprocessing.Process(target=run_flask, args=())
    process.start()
    time.sleep(0.5)
    yield 'http://127.0.0.1:8000'
    process.terminate()
