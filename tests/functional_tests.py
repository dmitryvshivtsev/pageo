from base_page.tests.test_page.test_page import TestPage


def test_caption(driver, url):
    page = TestPage(driver=driver, base_url=url)
    page.go_to_site()
    page.check_caption()


def test_paragraphs(driver, url):
    page = TestPage(driver=driver, base_url=url)
    page.go_to_site()
    page.check_paragraphs()

