from unittest.mock import MagicMock, patch, Mock
from urllib.parse import urljoin

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from pageo import BasePage
from pageo import IdLocator
from pageo.errors import DoublePageDefenitionError


base_url_test = "https://test.com"


class MockDriver:
    def set_window_size(self, screen_width, screen_height):
        pass

    def get(self, url):
        pass

    def find_element(self, by, selector):
        return selector


def test_inherit_with_locator():
    selector = 'test-id'

    class A_inherit_with_locator(BasePage):
        locator_1 = IdLocator(selector)

    class B_inherit_with_locator(A_inherit_with_locator):
        pass

    object_b = B_inherit_with_locator(driver=MockDriver(), base_url='https://test.com')

    assert object_b.locators['locator_1'] is not None
    assert object_b.locators['locator_1'] == selector
    assert object_b['locator_1'] == selector
    assert object_b.get_locator('locator_1') == selector


def test_inherit_with_too_similar_locators():
    first_selector = 'test-id'
    second_selector = 'abc'

    class A_inherit_with_too_similar_locators(BasePage):
        locator_1 = IdLocator(first_selector)

    class B_inherit_with_too_similar_locators(A_inherit_with_too_similar_locators):
        locator_1 = IdLocator(second_selector)

    object_b = B_inherit_with_too_similar_locators(driver=MockDriver(), base_url='https://test.com')

    assert object_b.locators['locator_1'] is not None
    assert object_b.locators['locator_1'] == second_selector
    assert object_b['locator_1'] == second_selector
    assert object_b.get_locator('locator_1') == second_selector


def test_inherit_with_too_similar_locators_and_another_one():
    first_selector = 'test-id'
    second_selector = 'abc'
    third_selector = 'def'

    class A_inherit_with_too_similar_locators_and_another_one(BasePage):
        locator_1 = IdLocator(first_selector)

    class B_inherit_with_too_similar_locators_and_another_one(A_inherit_with_too_similar_locators_and_another_one):
        locator_1 = IdLocator(second_selector)
        locator_2 = IdLocator(third_selector)

    object_b = B_inherit_with_too_similar_locators_and_another_one(driver=MockDriver(), base_url='https://test.com')

    assert object_b.locators['locator_1'] is not None
    assert object_b.locators['locator_1'] == second_selector
    assert object_b['locator_1'] == second_selector
    assert object_b.get_locator('locator_1') == second_selector

    assert object_b.locators['locator_2'] is not None
    assert object_b.locators['locator_2'] == third_selector
    assert object_b['locator_2'] == third_selector
    assert object_b.get_locator('locator_2') == third_selector


def test_get_inherited_classes():
    class A_get_inherited_classes(BasePage):
        pass

    class B_get_inherited_classes(A_get_inherited_classes):
        pass

    class C_get_inherited_classes(A_get_inherited_classes):
        pass

    assert A_get_inherited_classes in BasePage.get_inherited_classes()
    assert A_get_inherited_classes.get_inherited_classes() == [B_get_inherited_classes, C_get_inherited_classes]


def test_get_inherited_classes_without_inheritance():
    class Kek(BasePage):
        pass

    assert Kek.get_inherited_classes() == []


def test_ingerited_base_page_with_the_same_name():
    class A_ingerited_base_page_with_the_same_name(BasePage):
        pass

    with pytest.raises(DoublePageDefenitionError):
        class A_ingerited_base_page_with_the_same_name(BasePage):
            pass


@pytest.fixture
def base_page():
    """
    Фикстура, возвращающая экземпляр класса страницы и устанавливающая необходимые настройки драйвера.
    """
    driver = Mock()
    url_suffix = "/test"
    window_size = (1920, 1080)
    return BasePage(driver=driver, base_url=base_url_test, window_size=window_size, url_suffix=url_suffix)


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
    Тест проверяет, что метод перехода на страницу сайта вызывается с верными параметрами внутри конструктора.
    """
    base_page.driver.get.assert_called_once_with(base_page.url)


@patch.object(WebDriverWait, 'until')
def test_find_element(mock_until, base_page):
    locator = (By.ID, "test_id")
    mock_element = Mock()
    mock_until.return_value = mock_element

    element = base_page.find_element(*locator)

    mock_until.assert_called_once()
    assert element == mock_element


@patch.object(WebDriverWait, 'until')
def test_find_element_timeout_exception(mock_until, base_page):
    locator = (By.ID, "test_id")
    mock_until.side_effect = TimeoutException("Element not found")

    with pytest.raises(TimeoutException):
        base_page.find_element(*locator)


@patch.object(WebDriverWait, 'until')
def test_find_element_type_exception(mock_until, base_page):
    locator = 123
    mock_until.side_effect = TypeError("Invalid argument")

    with pytest.raises(TypeError):
        base_page.find_element(locator)


@patch.object(WebDriverWait, 'until')
def test_find_elements(mock_until, base_page):
    locator = (By.CLASS_NAME, "test_class")
    mock_elements = [Mock(), Mock()]
    mock_until.return_value = mock_elements

    elements = base_page.find_elements(*locator)

    mock_until.assert_called_once()
    assert elements == mock_elements


@patch.object(WebDriverWait, 'until')
def test_find_elements_timeout_exception(mock_until, base_page):
    locator = (By.CLASS_NAME, "test_class")
    mock_until.side_effect = TimeoutException("Element not found")

    with pytest.raises(TimeoutException):
        base_page.find_elements(*locator)

    mock_until.assert_called_once()


@patch.object(WebDriverWait, 'until')
def test_find_elements_type_exception(mock_until, base_page):
    locator = 123
    mock_until.side_effect = TypeError("Invalid argument")

    with pytest.raises(TypeError):
        base_page.find_elements(locator)


@patch.object(WebDriverWait, 'until')
def test_custom_wait_until(mock_until, base_page):
    condition = Mock()
    mock_until.return_value = condition

    base_page.custom_wait_until(condition)

    mock_until.assert_called_once()


@patch.object(WebDriverWait, 'until')
def test_custom_wait_until_timeout_exception(mock_until, base_page):
    mock_until.side_effect = TimeoutException("Element not found")

    with pytest.raises(TimeoutException):
        base_page.find_elements('', '')

    mock_until.assert_called_once()


@patch.object(ActionChains, 'move_to_element')
def test_my_function(mock_move_to_element, base_page):
    element = MagicMock()
    base_page.move_to_element(element)
    mock_move_to_element.assert_called_once()

