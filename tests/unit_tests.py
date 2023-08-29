from pageo.base_page import BasePage
from urllib.parse import urljoin
from unittest.mock import Mock, patch, MagicMock

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


base_url_test = "https://test.com"


@pytest.fixture
def base_page():
    """
    Фикстура, возвращающая экземпляр класса страницы и устанавливающая необходимые настройки драйвера.
    """
    driver = Mock()
    url_suffix = "/test"
    window_size = (1920, 1080)
    return BasePage(driver_fabric=driver, base_url=base_url_test, window_size=window_size, url_suffix=url_suffix)


def test_init(base_page):
    """
    Тест проверяет, что объект был создан корректно и аттрибуты объекта соответствуют ожидаемым.
    """
    assert base_page.driver is not None
    assert base_page.base_url == base_url_test
    assert base_page.url_suffix == "/test"
    assert base_page.url == urljoin(base_page.base_url, base_page.url_suffix)
    base_page.driver.set_window_size.assert_called_once_with(1920, 1080)


def test_go_to_site(base_page):
    """
    Тест проверяет, что метод перехода на страницу сайта вызывается с верными параметрами.
    """
    base_page.go_to_site()
    base_page.driver.get.assert_called_once_with(base_page.url)


@patch.object(WebDriverWait, 'until')
def test_find_element(mock_until, base_page):
    locator = (By.ID, "test_id")
    mock_element = Mock()
    mock_until.return_value = mock_element

    element = base_page.find_element(locator)

    mock_until.assert_called_once()
    assert element == mock_element


@patch.object(WebDriverWait, 'until')
def test_find_element_timeout_exception(mock_until, base_page):
    locator = (By.ID, "test_id")
    mock_until.side_effect = TimeoutException("Element not found")

    with pytest.raises(TimeoutException):
        base_page.find_element(locator)

    mock_until.assert_called_once()


@patch.object(WebDriverWait, 'until')
def test_find_element_type_exception(mock_until, base_page):
    locator = 123
    mock_until.side_effect = TypeError("Invalid argument")

    with pytest.raises(TypeError):
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
def test_find_elements_timeout_exception(mock_until, base_page):
    locator = (By.CLASS_NAME, "test_class")
    mock_until.side_effect = TimeoutException("Element not found")

    with pytest.raises(TimeoutException):
        base_page.find_elements(locator)

    mock_until.assert_called_once()


@patch.object(WebDriverWait, 'until')
def test_find_elements_type_exception(mock_until, base_page):
    locator = 123
    mock_until.side_effect = TypeError("Invalid argument")

    with pytest.raises(TypeError):
        base_page.find_elements(locator)

    mock_until.assert_called_once()


@patch.object(WebDriverWait, 'until')
def test_custom_wait_until(mock_until, base_page):
    condition = Mock()
    mock_until.return_value = condition

    base_page.custom_wait_until(condition)

    mock_until.assert_called_once()


@patch.object(WebDriverWait, 'until')
def test_custom_wait_until_timeout_exception(mock_until, base_page):
    condition = Mock()
    mock_until.side_effect = TimeoutException("Element not found")

    with pytest.raises(TimeoutException):
        base_page.find_elements(condition)

    mock_until.assert_called_once()


@patch.object(ActionChains, 'move_to_element')
def test_my_function(mock_move_to_element, base_page):
    element = MagicMock()
    base_page.move_to_element(element)
    mock_move_to_element.assert_called_once()



