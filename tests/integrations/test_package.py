from tests.integrations import TestPage


def test_caption_with_locator(driver, local_server_url):
    """
    Тест создает экземпляр страницы TestPage и проверяет, что текст в элементе
    с классом 'caption' на тестовой странице соответствует ожидаемому.
    """
    page = TestPage(driver=driver, base_url=local_server_url)
    actual_caption = page.get_caption_text()
    expected_caption = 'caption'
    assert actual_caption == expected_caption


def test_paragraphs_with_locator(driver, local_server_url):
    """
    Тест создает экземпляр страницы TestPage и проверяет, что тексты в элементах
    с классом 'paragraphs' на тестовой странице соответствует ожидаемому.
    """
    page = TestPage(driver=driver, base_url=local_server_url)
    actual_paragraph_texts = page.get_paragraph_texts()
    expected_paragraph_texts = ['first_paragraph', 'second_paragraph']
    assert actual_paragraph_texts == expected_paragraph_texts


def test_caption_with_find_elements(driver, local_server_url):
    """
    Тест создает экземпляр страницы TestPage и проверяет, что текст в элементе
    с классом 'caption' на тестовой странице соответствует ожидаемому.
    """
    page = TestPage(driver=driver, base_url=local_server_url)
    actual_caption_list = page.get_caption_text_list()
    expected_caption = 'caption'
    assert isinstance(actual_caption_list, list)

    actual_caption = actual_caption_list[0].text
    assert actual_caption == expected_caption


def test_paragraphs_with_find_elements(driver, local_server_url):
    """
    Тест создает экземпляр страницы TestPage и проверяет, что тексты в элементах
    с классом 'paragraphs' на тестовой странице соответствует ожидаемому.
    """
    page = TestPage(driver=driver, base_url=local_server_url)
    actual_paragraph_texts = page.get_paragraph_texts_list()
    expected_paragraph_texts = ['first_paragraph', 'second_paragraph']
    assert actual_paragraph_texts == expected_paragraph_texts

