from selenium import webdriver


def test_fixture_driver(driver):
    assert isinstance(driver, webdriver.Chrome)


def test_fixture_options(chrome_options):
    assert isinstance(chrome_options, webdriver.ChromeOptions)


def test_fixture_url(url):
    assert url == 'http://127.0.0.1:3000'
