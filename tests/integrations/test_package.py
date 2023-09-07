from tests.integrations import TestPage


def test_caption(driver, url):
    """
    Тест создает экземпляр страницы TestPage и проверяет, что текст в элементе
    с классом 'caption' на тестовой странице соответствует ожидаемому.
    """
    page = TestPage(driver=driver, base_url=url)
    actual_caption = page.get_caption_text()
    expected_caption = 'caption'
    assert actual_caption == expected_caption


def test_paragraphs(driver, url):
    """
    Тест создает экземпляр страницы TestPage и проверяет, что тексты в элементах
    с классом 'paragraphs' на тестовой странице соответствует ожидаемому.
    """
    page = TestPage(driver=driver, base_url=url)
    actual_paragraph_texts = page.get_paragraph_texts()
    expected_paragraph_texts = ['first_paragraph', 'second_paragraph']
    assert actual_paragraph_texts == expected_paragraph_texts
