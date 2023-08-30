from selenium.webdriver.common.by import By

from pageo.locators.abstract_locator import AbstractLocator


class NameLocator(AbstractLocator):
    """
    Класс локатора, выполняющий поиск на основе аттрибута name у тега элемента.
    """
    by = By.NAME
