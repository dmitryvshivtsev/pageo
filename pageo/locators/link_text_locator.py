from selenium.webdriver.common.by import By

from pageo.locators.abstract_locator import AbstractLocator


class LinkTextLocator(AbstractLocator):
    """
    Класс локатора, выполняющий поиск на основе текста внутри ссылки элемента.
    """
    by = By.LINK_TEXT
