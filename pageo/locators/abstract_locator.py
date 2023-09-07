from abc import ABC


class AbstractLocator(ABC):
    """
    Вспомогательный абстрактный класс для BasePage, инкапсулирующий логику поиска
    элементов по локаторам.

    Класс работает через протокол дескрипторов. Экземпляр отнаследованного класса представляет один
    локатор, скрывая логику поиска элементов.

    Пример использования наследника в связке с BasePage:
    >>> from pageo.base_page import BasePage
    >>> from pageo.locators.id_locator import IdLocator
    >>>
    >>>
    >>> class AboutPage(BasePage):
    ...     search_field_element = IdLocator("id-search-field")
    ...     def is_search_field(self):
    ...         return True if self.search_field_element else False
    """
    def __init__(self, selector: str, is_many: bool = False, timeout: int = 5):
        self.selector = selector
        self.is_many = is_many
        self.timeout = timeout

    def __get__(self, instance, owner=None):
        if self.is_many:
            return instance.find_elements(self.by, self.selector, self.timeout)
        return instance.find_element(self.by, self.selector, self.timeout)

    def set_name(self, name):
        self.name = name
