from core_page.base_page import BasePage

import pytest
from unittest.mock import Mock, patch
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def base_page():
    driver = Mock()
    url_suffix = "/test"
    window_size = (1920, 1080)
    return BasePage(driver, window_size, url_suffix)


def test_init(base_page):
    assert base_page.driver is not None
    assert base_page.base_url == "https://test.com"
    assert base_page.url_suffix == "/test"
    assert base_page.url == "https://test.com"
    base_page.driver.set_window_size.assert_called_once_with(1920, 1080)


def test_go_to_site(base_page):
    base_page.go_to_site()
    base_page.driver.get.assert_called_once_with("https://expert.vk.com/test")


@patch.object(WebDriverWait, 'until')
def test_find_element(mock_until, base_page):
    locator = (By.ID, "test_id")
    mock_element = Mock()
    mock_until.return_value = mock_element

    element = base_page.find_element(locator)

    mock_until.assert_called_once()
    assert element == mock_element


@patch.object(WebDriverWait, 'until')
def test_find_element_exception(mock_until, base_page):
    locator = (By.ID, "test_id")
    mock_until.side_effect = TimeoutException("Element not found")

    with pytest.raises(TimeoutException):
        base_page.find_element(locator)

    mock_until.assert_called_once()


@patch.object(WebDriverWait, 'until')
def test_find_elements(mock_until, base_page):
    locator = (By.CLASS_NAME, "test_class")
    mock_elements = [Mock(), Mock()]
    mock_until.return_value = mock_elements

    elements = base_page.find_elements(locator)

    mock_until.assert_called_once()
    assert elements == mock_elements


@patch.object(WebDriverWait, 'until')
def test_find_elements_exception(mock_until, base_page):
    locator = (By.CLASS_NAME, "test_class")
    mock_until.side_effect = TimeoutException("Element not found")

    with pytest.raises(TimeoutException):
        base_page.find_element(locator)

    mock_until.assert_called_once()
