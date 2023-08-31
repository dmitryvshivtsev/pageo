from pageo import BasePage
from pageo.locators import ClassNameLocator


class TestPage(BasePage):
    __test__ = False
    caption_element = ClassNameLocator(selector="caption")
    paragraph_elements = ClassNameLocator(selector="paragraphs", is_many=True)

    def check_caption(self):
        actual_caption = self.caption_element.text
        assert actual_caption == 'caption'

    def check_paragraphs(self):
        actual_paragraphs = self.paragraph_elements
        expected_paragraph_texts = ('first_paragraph', 'second_paragraph')
        for actual_paragraph, expected_paragraph in zip(actual_paragraphs, expected_paragraph_texts):
            assert actual_paragraph.text == expected_paragraph
