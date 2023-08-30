from selenium.webdriver.common.by import By

from pageo.locators.abstract_locator import AbstractLocator


class IdLocator(AbstractLocator):
    """
    Класс локатора, выполняющий поиск на основе аттрибута id у тега элемента.
    """
    by = By.ID
