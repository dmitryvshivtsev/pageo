from selenium.webdriver.common.by import By

from pageo.locators.abstract_locator import AbstractLocator


class CSSLocator(AbstractLocator):
    """
    Класс представляет собой объект локатора,
    который создается на основе css-локатора элемента.
    """

    by = By.CSS_SELECTOR
