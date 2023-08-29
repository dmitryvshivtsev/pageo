from selenium.webdriver.common.by import By

from pageo.locators.abstract_locator import AbstractLocator


class TagNameLocator(AbstractLocator):
    """
    Класс представляет собой объект локатора,
    который создается на основе id атрибута элемента
    """
    by = By.TAG_NAME
