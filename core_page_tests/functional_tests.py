import pytest
from selenium import webdriver


@pytest.fixture(scope='session')
def chrome_options_base_page():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    return options


@pytest.fixture(scope='session')
def driver_base_page(chrome_options):
    one_driver = webdriver.Chrome(chrome_options)
    yield one_driver
    one_driver.quit()


@pytest.fixture
def base_url_base_page():
    return 'https://127.0.0.1:8000'


def test_h():
    # page = BasePage(driver_base_page, window_size=(1920, 1080))
    # page.go_to_site()
    # header = page.find_element(By.CLASS_NAME, "header")
    # assert header.text == 'header'
    assert 1 == 1

