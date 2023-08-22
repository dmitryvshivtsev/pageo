from core_page.core_page_tests.test_page.test_page import TestPage


def test_caption():
    page = TestPage()
    page.go_to_site()
    page.check_caption()


def test_paragraphs():
    page = TestPage()
    page.go_to_site()
    page.check_paragraphs()

