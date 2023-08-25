from core_page.base_page.base_page import BasePage

from selenium.webdriver.common.by import By


class TestPage(BasePage):
    __test__ = False

    def check_caption(self):
        actual_caption = self.find_element((By.CLASS_NAME, "caption")).text
        assert actual_caption == 'caption'

    def check_paragraphs(self):
        actual_paragraphs = self.find_elements((By.CLASS_NAME, "paragraphs"))
        expected_paragraph_texts = ('first_paragraph', 'second_paragraph')
        for actual_paragraph, expected_paragraph in zip(actual_paragraphs, expected_paragraph_texts):
            assert actual_paragraph.text == expected_paragraph
