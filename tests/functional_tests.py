from core_page.tests.test_page.test_page import TestPage


base_url_test = "http://127.0.0.1:8000"


def test_caption():
    page = TestPage(base_url=base_url_test)
    page.go_to_site()
    page.check_caption()


def test_paragraphs():
    page = TestPage(base_url=base_url_test)
    page.go_to_site()
    page.check_paragraphs()

