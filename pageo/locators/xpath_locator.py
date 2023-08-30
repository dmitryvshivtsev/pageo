from selenium.webdriver.common.by import By

from pageo.locators.abstract_locator import AbstractLocator


class XPATHLocator(AbstractLocator):
    """
    Класс локатора, выполняющий поиск на основе пути XPath до элемента.
    """
    by = By.XPATH
