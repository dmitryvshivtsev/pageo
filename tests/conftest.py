import multiprocessing

import pytest
from selenium import webdriver

from tests.flask_app import run_flask


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


@pytest.fixture(scope='session')
def url():
    """
    Фикстура создает и запускает процесс, выполняющий запуск сервера Flask.
    Возвращает url на котором запущен сервер. После выполнения тестов процесс завершается.
    """
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=run_flask, args=(queue, ))
    process.start()
    queue.get()
    yield 'http://127.0.0.1:3000'
    process.terminate()

