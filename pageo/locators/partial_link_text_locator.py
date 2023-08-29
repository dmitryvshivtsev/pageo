from selenium.webdriver.common.by import By

from pageo.locators.abstract_locator import AbstractLocator


class PartialLinkTextLocator(AbstractLocator):
    """
    Класс представляет собой объект локатора,
    который создается на основе вхождения текста внутри ссылки элемента
    """
    by = By.PARTIAL_LINK_TEXT
