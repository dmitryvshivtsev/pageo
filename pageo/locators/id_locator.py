from selenium.webdriver.common.by import By

from pageo.locators.abstract_locator import AbstractLocator


class IdLocator(AbstractLocator):
    """
    Класс представляет собой объект локатора,
    которые
    """
    by = By.ID
