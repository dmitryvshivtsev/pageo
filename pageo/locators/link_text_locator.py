from selenium.webdriver.common.by import By

from pageo.locators.abstract_locator import AbstractLocator


class LinkTextLocator(AbstractLocator):
    """
    Класс представляет собой объект локатора,
    который создается на основе текста внутри ссылки элемента.
    """
    by = By.LINK_TEXT
