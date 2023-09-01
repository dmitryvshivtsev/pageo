from pageo import BasePage
from pageo.locators import ClassNameLocator


class TestPage(BasePage):
    """
    Класс тестовой страницы, которая открывается при запуске сервера Flask. Содержит методы, которые
    взаимодействуют с элементами на странице.

    Класс предназначен для объединения различных модулей
    в единую группу и их последующего тестирования.
    """
    __test__ = False

    caption_element = ClassNameLocator(selector="caption")
    paragraph_elements = ClassNameLocator(selector="paragraphs", is_many=True)

    def get_caption_text(self) -> str:
        """ Возвращает текст элемента caption_element. """
        return self.caption_element.text

    def get_paragraph_texts(self) -> list:
        """ Возвращает список, содержащий тексты всех найденных элементов из paragraph_elements. """
        actual_paragraphs = self.paragraph_elements
        actual_paragraph_texts = [paragraph.text for paragraph in actual_paragraphs]
        return actual_paragraph_texts
