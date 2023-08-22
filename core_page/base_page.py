import os
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Базовый класс для взаимодействия с любой страницей.
    Содержит общие методы для взаимодействия с элементами на страницах любого веб-сайта.
    """
    def __init__(self,
                 driver=webdriver.Chrome(),
                 base_url=os.environ.get('BASE_URL'),
                 window_size=(1920, 1080),
                 url_suffix=''
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
        self.driver = driver
        self.base_url = base_url
        self.url_suffix = url_suffix
        self.url = urljoin(self.base_url, self.url_suffix)
        screen_width, screen_height = window_size
        self.driver.set_window_size(screen_width, screen_height)

    def find_element(self, locator, duration=5):
        """
        Метод, для поиска элемента на странице, с использованием явного ожидания.
        :param locator: Локатор элемента, который необходимо найти.
        :param duration: Время, в течение которого будет ожидаться появление элемента. По умолчанию 5 секунд.
        :return: Объект WebElement, если элемент найден на странице.
        Иначе, возвращает TimeoutException с дополнительным сообщением.
        """
        return WebDriverWait(self.driver, duration).until(EC.presence_of_element_located(locator),
                                                          message=f"Не найден элемент с локатором {locator}")

    def find_elements(self, locator, duration=5):
        """
        Метод, для поиска элементов на странице, с использованием явного ожидания.
        :param locator: Локатор элементов, которые необходимо найти.
        :param duration: Время, в течение которого будет ожидаться появление элементов. По умолчанию 5 секунд.
        :return: Список объектов WebElement, если элементы найдены на странице.
        Иначе, возвращает TimeoutException с дополнительным сообщением.
        """
        return WebDriverWait(self.driver, duration).until(EC.presence_of_all_elements_located(locator),
                                                          message=f"Не найдены элементы с локатором  {locator}")

    def go_to_site(self):
        """
        Метод, для перехода на страницу сайта по заданному адресу.
        """
        self.driver.get(self.url)
