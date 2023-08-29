from abc import ABC


class AbstractLocator(ABC):
    """
    Вспомогательный абстрактный класс для BasePage, инкапсулирующий логику поиска
    элементов по локаторам.

    Класс работает через протокол дескрипторов. Экземпляр отнаследованного класса представляет один
    локатор, скрывая логику поиска элементов.

    Пример использования наследника в связке с BasePage:
    >>>
    """
    def __init__(self, selector: str, is_many: bool = False):
        self.selector = selector
        self.is_many = is_many

    def __get__(self, instance, owner=None):
        if self.is_many:
            return instance.find_elements(self.by, self.selector)
        return instance.find_element(self.by, self.selector)

    def set_name(self, name):
        self.name = name

