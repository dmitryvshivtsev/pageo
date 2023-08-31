from threading import Lock
from typing import Callable, Hashable, List
from functools import cached_property
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageo.locators.abstract_locator import AbstractLocator
from pageo.utils.map_dict import MapDict


class DoublePageDefenitionError(Exception):
    pass


class MetaBasePage(type):
    lock = Lock()

    def __new__(mcls, name, bases, attrs):
        class_instance = super(MetaBasePage, mcls).__new__(mcls, name, bases, attrs)
        if len(class_instance.__mro__) > 2:
            parent_class = class_instance.__mro__[1]
            with mcls.lock:
                if not 'inherited_classes' in parent_class.__dict__:
                    parent_class.inherited_classes = {}
                if parent_class.inherited_classes.get(name) is not None:
                    raise DoublePageDefenitionError("You can't to define two classes with the same name.")
                parent_class.inherited_classes[name] = class_instance
        return class_instance


class BasePage(metaclass=MetaBasePage):
    """
    Базовый класс для взаимодействия с любой страницей.
    Содержит общие методы для взаимодействия с элементами на страницах любого веб-сайта.
    """

    def __init__(
            self,
            base_url: str,
            driver: webdriver,
            window_size: tuple = (1920, 1080),
            url_suffix: str = '',
    ):
        """
        Конструктор класса, выполняющий функцию установки различных настроек.
        1. Указывает драйвер для последующей работы с selenium;
        2. Собирает url страницы, на которую нужно осуществить последующий переход;
        3. Устанавливает размер экрана страницы браузера.
        :param driver: Selenium-драйвер. Используется для доступа к методам работы со страницей.
        :param url_suffix: Относительный путь к конкретной странице.
        :param window_size: Размер окна для тестирования на различных устройствах.
        """
        self.driver_fabric = lambda: driver
        self.base_url = base_url
        self.url_suffix = url_suffix
        self.url = urljoin(self.base_url, self.url_suffix)
        screen_width, screen_height = window_size
        self.driver.set_window_size(screen_width, screen_height)
        self.open()

        mro_dicts = {}
        for Class in reversed(type(self).__mro__):
            mro_dicts.update(Class.__dict__)
        self.locators = MapDict(
            mro_dicts,
            lambda x: x.__get__(self),
        )

        for name, value in self.__class__.__dict__.items():
            if isinstance(value, AbstractLocator):
                value.set_name(name)

    @cached_property
    def driver(self) -> WebDriver:
        return self.driver_fabric()

    @classmethod
    def with_driver_fabric(cls, base_url: str, driver_fabric: Callable[[], WebDriver] = webdriver.Chrome, *args,
                           **kwargs) -> 'BasePage':
        """
        Создает экземпляр класса BasePage с переданным драйвером.
        """
        page_object = cls(base_url, driver=None, *args, **kwargs)
        page_object.driver_fabric = driver_fabric
        return page_object

    @classmethod
    def get_inherited_classes(cls) -> List['BasePage']:
        return list(cls.__dict__.get('inherited_classes', {}).values())

    def __getitem__(self, key: str) -> WebElement:
        return self.get_locator(key)

    def get_locator(self, name: str) -> WebElement:
        return self.locators[name]

    def find_element(self, by: str, selector: str, duration: int = 5) -> WebElement:
        """
        Метод, для поиска элемента на странице, с использованием явного ожидания.
        :param by: Стратегия для поиска элемента.
        :param selector: Селектор элемента, который необходимо найти.
        :param duration: Время, в течение которого будет ожидаться появление элемента. По умолчанию 5 секунд.
        :return: Объект WebElement, если элемент найден на странице.
        Иначе, возвращает TimeoutException с дополнительным сообщением.
        """
        return WebDriverWait(self.driver, duration).until(EC.presence_of_element_located((by, selector)),
                                                          message=f"Не найден элемент со стратегией локатора {by} и с селектором {selector}")

    def find_elements(self, by: str, selector: str, duration: int = 5) -> WebElement:
        """
        Метод, для поиска элементов на странице, с использованием явного ожидания.
        :param by: Стратегия для поиска элементов.
        :param selector: Селектор элементов, которые необходимо найти.
        :param duration: Время, в течение которого будет ожидаться появление элементов. По умолчанию 5 секунд.
        :return: Список объектов WebElement, если элементы найдены на странице.
        Иначе, возвращает TimeoutException с дополнительным сообщением.
        """
        return WebDriverWait(self.driver, duration).until(EC.presence_of_all_elements_located((by, selector)),
                                                          message=f"Не найдены элементы со стратегией локатора {by} и с селектором {selector}")

    def open(self) -> None:
        """
        Метод, для перехода на страницу сайта по заданному адресу.
        """
        self.driver.get(self.url)

    def custom_wait_until(self, func_condition: Callable, duration: int = 5) -> None:
        """
        Метод позволяет задавать ожидания на основе
        пользовательских условий.

        В случае, когда условие ожидания, которое нам нужно, не предусмотрено selenium, пользователь
        может сам задать условие ожидания на основе какой-либо функции.

        Например: lambda browser: len(browser.window_handles) != 2 задаст следующие условие ожидания: ждем пока
        количество вкладок в браузере не станет равным двум.

        :param func_condition: Функция предикат, в которой задано условие ожидания.
        :param duration: Числовое значение в секундах, используемое для передачи его в явное ожидания.
        """
        WebDriverWait(self.driver, duration).until(func_condition)

    def move_to_element(self, element: WebElement) -> None:
        """
        Имитирует наведение мыши на элемент.

        :param element: Какой-либо WebElement.
        """
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()
