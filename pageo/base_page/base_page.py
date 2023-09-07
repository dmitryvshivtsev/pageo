from typing import Callable, List, Any
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageo.base_page.meta_base_page import MetaBasePage
from pageo.locators.abstract_locator import AbstractLocator
from pageo.utils.map_dict import MapDict
from pageo.utils.protocol_setter import get_base_url_with_protocol
from pageo.errors import UrlAvailabilityError, UrlDisparityError


class BasePage(metaclass=MetaBasePage):
    """
    Базовый класс для взаимодействия с любой страницей.
    Содержит общие методы для взаимодействия с элементами на страницах любого веб-сайта.
    """
    base_url: str = None
    url_suffix: str = None

    def __init__(
            self,
            driver: webdriver,
            base_url: str = None,
            url_suffix: str = None,
            window_size: tuple = (1920, 1080),
    ):
        """
        Конструктор класса, выполняющий функцию установки различных настроек.
        1. Указывает драйвер для последующей работы с selenium;
        2. Собирает url страницы, на которую нужно осуществить последующий переход;
        3. Устанавливает размер экрана страницы браузера.
        :param driver: Selenium-драйвер. Используется для доступа к методам работы со страницей.
        :param base_url: Базовый url страницы.
        :param url_suffix: Относительный путь к конкретной странице.
        :param window_size: Размер окна для тестирования на различных устройствах.
        """

        if self.base_url is None and base_url is None:
            raise UrlAvailabilityError("You have to create a 'base_url' in the class attribute"
                                       " or set the url when creating the object")
        elif (self.base_url is not None and base_url is not None) and self.base_url != base_url:
            raise UrlDisparityError("'base_url' in class attributes and in class arguments are different. "
                                    "Specify one URL in class attributes or in arguments")
        elif base_url is not None:
            self.base_url = get_base_url_with_protocol(base_url)

        if (self.url_suffix is not None and url_suffix is not None) and self.url_suffix != url_suffix:
            raise UrlDisparityError("'url_suffix' in class attributes and in class arguments are different. "
                                    "Specify one 'url_suffix' in class attributes or in arguments")
        elif url_suffix is not None:
            self.url_suffix = url_suffix

        self.driver = driver
        self.url = urljoin(get_base_url_with_protocol(self.base_url), self.url_suffix)
        self.screen_width, self.screen_height = window_size
        self.driver.set_window_size(self.screen_width, self.screen_height)
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

    @classmethod
    def get_inherited_classes(cls) -> List['BasePage']:
        return list(cls.__dict__.get('inherited_classes', {}).values())

    def get_locator(self, name: str) -> WebElement:
        return self.locators[name]

    def __getitem__(self, key: str) -> WebElement:
        return self.get_locator(key)

    def __repr__(self):
        return f'{type(self).__name__}(base_url="{self.base_url}", ' \
               f'driver={repr(self.driver)}, ' \
               f'window_size={(self.screen_width, self.screen_height)}, ' \
               f'url_suffix="{self.url_suffix}")'

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
        Метод открывает страницу по заданному адресу.
        """
        self.driver.get(self.url)

    def custom_wait_until(self, func_condition: Callable[[], Any], duration: int = 5) -> None:
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
