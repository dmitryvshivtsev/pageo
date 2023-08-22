from core_page.tests.test_page.test_page import TestPage


def test_caption(url):
    page = TestPage(base_url=url)
    page.go_to_site()
    page.check_caption()


def test_paragraphs(url):
    page = TestPage(base_url=url)
    page.go_to_site()
    page.check_paragraphs()

