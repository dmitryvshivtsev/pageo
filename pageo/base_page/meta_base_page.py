from threading import Lock

from pageo.errors import DoublePageDefenitionError


class MetaBasePage(type):
    """
    Мета-класс для базового класса BasePage. Создает в классах страницы словарь, где:
    * Ключ - имя класса;
    * Значение - список унаследованных классов от класса, указанного в ключе.
    
    Также проверяет, что нет двух классов страниц с одинаковым именем.
    """
    lock = Lock()

    def __new__(mcls, name, bases, attrs):
        class_instance = super(MetaBasePage, mcls).__new__(mcls, name, bases, attrs)
        if len(class_instance.__mro__) > 2:
            parent_class = class_instance.__mro__[1]
            with mcls.lock:
                if 'inherited_classes' not in parent_class.__dict__:
                    parent_class.inherited_classes = {}
                if parent_class.inherited_classes.get(name) is not None:
                    raise DoublePageDefenitionError("You can't to define two classes with the same name.")
                parent_class.inherited_classes[name] = class_instance
        return class_instance
