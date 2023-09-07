from unittest.mock import MagicMock, patch, Mock
from urllib.parse import urljoin

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from pageo import BasePage
from pageo import IdLocator
from pageo.errors import DoublePageDefenitionError, UrlAvailabilityError, UrlDisparityError
from pageo.utils.protocol_setter import get_base_url_with_protocol

base_url_test = "https://test.com"


class MockDriver:
    """
    Класс для имитации драйвера.
    """

    def set_window_size(self, screen_width, screen_height):
        pass

    def get(self, url):
        pass

    def find_element(self, by, selector):
        return selector


def test_inherit_with_locator():
    """
    Тест проверяет видимость локаторов в классе наследнике от класса, унаследованного от BasePage.
    """
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
    """
    Тест проверяет, что локатор изменяется в классе наследнике от класса, унаследованного от BasePage,
    в котором был объявлен этот локатор.
    """
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
    """
    Тест проверяет, что:
    1. Локатор изменяется в классе наследнике от класса, унаследованного от BasePage, в котором был объявлен этот локатор;
    2. Доступен новый локатор, объявленный в классе наследнике.
    """
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
    """
    Тест проверяет, что:
    1. Метод класса get_inherited_classes() возвращает список, в котором присутствует класс, унаследованный от BasePage;
    2. В списке также присутствуют классы наследники от класса, который является наследником BasePage.
    """

    class A_get_inherited_classes(BasePage):
        pass

    class B_get_inherited_classes(A_get_inherited_classes):
        pass

    class C_get_inherited_classes(A_get_inherited_classes):
        pass

    assert A_get_inherited_classes in BasePage.get_inherited_classes()
    assert A_get_inherited_classes.get_inherited_classes() == [B_get_inherited_classes, C_get_inherited_classes]


def test_get_inherited_classes_without_inheritance():
    """
    Тест проверяет, что для класса наследника от BasePage список наследников пустой.
    """

    class Kek(BasePage):
        pass

    assert Kek.get_inherited_classes() == []


def test_inherited_base_page_with_the_same_name():
    """
    Тест проверяет, что при наличии двух классов с одинаковым именем, выбрасывается исключение DoublePageDefenitionError.
    """

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
    assert base_page.base_url == get_base_url_with_protocol(base_url_test)
    assert base_page.url_suffix == "/test"
    assert base_page.url == urljoin(base_page.base_url, base_page.url_suffix)
    base_page.driver.set_window_size.assert_called_once_with(1920, 1080)


def test_open(base_page):
    """
    Тест проверяет, что метод перехода на страницу сайта вызывается с верными параметрами внутри конструктора.
    """
    base_page.driver.get.assert_called_once_with(base_page.url)


@patch.object(WebDriverWait, 'until')
def test_find_element(mock_until, base_page):
    """
    Тест проверяет, что метод find_element() работает корректно и внутри него срабатывает явное ожидание.
    """
    locator = (By.ID, "test_id")
    mock_element = Mock()
    mock_until.return_value = mock_element

    element = base_page.find_element(*locator)

    mock_until.assert_called_once()
    assert element == mock_element


@patch.object(WebDriverWait, 'until')
def test_find_element_timeout_exception(mock_until, base_page):
    """
    Тест проверяет, что метод find_element() выбрасывает исключение, если элемент не найден.
    """
    locator = (By.ID, "test_id")
    mock_until.side_effect = TimeoutException("Element not found")

    with pytest.raises(TimeoutException):
        base_page.find_element(*locator)


@patch.object(WebDriverWait, 'until')
def test_find_element_type_exception(mock_until, base_page):
    """
    Тест проверяет, что метод find_element() выбрасывает исключение, если переданы неверные аргументы.
    """
    locator = 123
    mock_until.side_effect = TypeError("Invalid argument")

    with pytest.raises(TypeError):
        base_page.find_element(locator)


@patch.object(WebDriverWait, 'until')
def test_find_elements(mock_until, base_page):
    """
    Тест проверяет, что метод find_elements() работает корректно и внутри него срабатывает явное ожидание.
    """
    locator = (By.CLASS_NAME, "test_class")
    mock_elements = [Mock(), Mock()]
    mock_until.return_value = mock_elements

    elements = base_page.find_elements(*locator)

    mock_until.assert_called_once()
    assert elements == mock_elements


@patch.object(WebDriverWait, 'until')
def test_find_elements_timeout_exception(mock_until, base_page):
    """
    Тест проверяет, что метод find_elements() выбрасывает исключение, если элемент не найден.
    """
    locator = (By.CLASS_NAME, "test_class")
    mock_until.side_effect = TimeoutException("Element not found")

    with pytest.raises(TimeoutException):
        base_page.find_elements(*locator)

    mock_until.assert_called_once()


@patch.object(WebDriverWait, 'until')
def test_find_elements_type_exception(mock_until, base_page):
    """
    Тест проверяет, что метод find_elements() выбрасывает исключение, если переданы неверные аргументы.
    """
    locator = 123
    mock_until.side_effect = TypeError("Invalid argument")

    with pytest.raises(TypeError):
        base_page.find_elements(locator)


@patch.object(WebDriverWait, 'until')
def test_custom_wait_until(mock_until, base_page):
    """
    Тест проверяет, что метод custom_wait_until() вызывает явное ожидание до тех пор, пока не будет выполнено условие.
    """
    condition = Mock()
    mock_until.return_value = condition

    base_page.custom_wait_until(condition)

    mock_until.assert_called_once()


@patch.object(WebDriverWait, 'until')
def test_custom_wait_until_timeout_exception(mock_until, base_page):
    """
    Тест проверяет, что в случае невыполнения условия в течение заданного времени, метод
    custom_wait_until() выбрасывает исключение TimeoutException.
    """
    mock_until.side_effect = TimeoutException("Element not found")

    with pytest.raises(TimeoutException):
        base_page.find_elements('', '')

    mock_until.assert_called_once()


@patch.object(ActionChains, 'move_to_element')
def test_move_to_element(mock_move_to_element, base_page):
    """
    Тест проверяет, что метод работает корректно и наведение мыши на элемент действительно происходит.
    """
    element = MagicMock()
    base_page.move_to_element(element)
    mock_move_to_element.assert_called_once()


def test_class_locator_with_single_element():
    """
    Тест проверяет, что класс локатора работает корректно и вызывает внутри себя find_element().
    """
    mock_instance = Mock()
    mock_instance.find_element.return_value = "element"
    locator = IdLocator("selector")
    result = locator.__get__(mock_instance)
    assert result == "element"
    mock_instance.find_element.assert_called_with(locator.by, locator.selector, locator.timeout)


def test_class_locator_with_multiple_elements():
    """
    Тест проверяет, что класс локатора работает корректно и вызывает внутри себя find_elements().
    """
    mock_instance = Mock()
    mock_instance.find_elements.return_value = ["element1", "element2"]
    locator = IdLocator("selector", is_many=True)
    result = locator.__get__(mock_instance)
    assert result == ["element1", "element2"]
    mock_instance.find_elements.assert_called_with(locator.by, locator.selector, locator.timeout)


def test_class_locator_set_name():
    """
    Тест проверяет, что метод set_name() в классе локатора работает корректно.
    """
    locator = IdLocator("selector")
    locator.set_name("LOL")
    assert locator.name == "LOL"


def test_base_url_class_attribute():
    class SomePage_test_base_url_class_attribute(BasePage):
        base_url = 'https://some_url.com'

    page = SomePage_test_base_url_class_attribute(driver=MockDriver())
    assert hasattr(page, 'base_url')
    assert page.base_url == 'https://some_url.com'


def test_base_url_class_arguments():
    class SomePage_test_base_url_class_arguments(BasePage):
        pass

    page = SomePage_test_base_url_class_arguments(driver=MockDriver(),
                                                  base_url='https://some_url.com')
    assert page.base_url == 'https://some_url.com'


def test_base_url_raise_url_not_specified():
    class SomePage_test_base_url_raise_url_not_specified(BasePage):
        pass

    with pytest.raises(UrlAvailabilityError):
        page = SomePage_test_base_url_raise_url_not_specified(driver=MockDriver())


def test_base_url_raise_url_different_in_arguments_and_attributes():
    class SomePage_test_base_url_different_in_arguments_and_attributes(BasePage):
        base_url = 'https://some_url.com'

    with pytest.raises(UrlDisparityError):
        page = SomePage_test_base_url_different_in_arguments_and_attributes(driver=MockDriver(),
                                                                            base_url='https://another_url.com')


def test_url_suffix_class_attribute():
    class SomePage_test_url_suffix_class_attribute(BasePage):
        base_url = 'https://some_url.com'
        url_suffix = '/some_page'

    page = SomePage_test_url_suffix_class_attribute(driver=MockDriver())
    assert hasattr(page, 'url_suffix')
    assert page.base_url == 'https://some_url.com'
    assert page.url_suffix == '/some_page'
    assert page.url == 'https://some_url.com/some_page'


def test_url_suffix_class_argument():
    class SomePage_test_url_suffix_class_argument(BasePage):
        base_url = 'https://some_url.com'

    page = SomePage_test_url_suffix_class_argument(driver=MockDriver(),
                                                   url_suffix='/some_page')
    assert hasattr(page, 'url_suffix')
    assert page.base_url == 'https://some_url.com'
    assert page.url_suffix == '/some_page'
    assert page.url == 'https://some_url.com/some_page'


def test_url_suffix_raise_suffix_different_in_arguments_and_attributes():
    class SomePage_test_url_suffix_raise_suffix_different_in_arguments_and_attributes(BasePage):
        base_url = 'https://some_url.com'
        url_suffix = '/some_page'

    with pytest.raises(UrlDisparityError):
        page = SomePage_test_url_suffix_raise_suffix_different_in_arguments_and_attributes(driver=MockDriver(),
                                                                                          url_suffix='/another_page')


def test_url_suffix_class_attribute_but_base_url_arguments():
    class SomePage_test_url_suffix_class_attribute_but_base_url_arguments(BasePage):
        url_suffix = '/some_page'

    page = SomePage_test_url_suffix_class_attribute_but_base_url_arguments(driver=MockDriver(),
                                                                           base_url='https://some_url.com')
    assert hasattr(page, 'url_suffix')
    assert page.base_url == 'https://some_url.com'
    assert page.url_suffix == '/some_page'
    assert page.url == 'https://some_url.com/some_page'
