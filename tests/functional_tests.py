from core_page.tests.test_page.test_page import TestPage


def test_caption(driver, url):
    page = TestPage.with_driver(driver=driver, base_url=url)
    page.go_to_site()
    page.check_caption()


def test_paragraphs(driver, url):
    page = TestPage.with_driver(driver=driver, base_url=url)
    page.go_to_site()
    page.check_paragraphs()

