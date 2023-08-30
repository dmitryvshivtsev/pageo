from selenium.webdriver.common.by import By

from pageo.locators.abstract_locator import AbstractLocator


class ClassNameLocator(AbstractLocator):
    """
    Класс локатора, выполняющий поиск на основе имени класса элемента.
    """
    by = By.CLASS_NAME

