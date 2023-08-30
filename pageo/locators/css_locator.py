from selenium.webdriver.common.by import By

from pageo.locators.abstract_locator import AbstractLocator


class CSSLocator(AbstractLocator):
    """
    Класс локатора, выполняющий поиск на основе css-локатора элемента.
    """
    by = By.CSS_SELECTOR
