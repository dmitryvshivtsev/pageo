from selenium.webdriver.common.by import By

from pageo.locators.abstract_locator import AbstractLocator


class TagNameLocator(AbstractLocator):
    """
    Класс локатора, выполняющий поиск на основе имени тега элемента.
    """
    by = By.TAG_NAME
