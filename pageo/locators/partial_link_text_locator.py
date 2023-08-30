from selenium.webdriver.common.by import By

from pageo.locators.abstract_locator import AbstractLocator


class PartialLinkTextLocator(AbstractLocator):
    """
    Класс локатора, выполняющий поиск на основе вхождения текста внутри ссылки элемента.
    """
    by = By.PARTIAL_LINK_TEXT
