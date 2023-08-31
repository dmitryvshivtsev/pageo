from tests.integrations import TestPage


def test_caption(driver, url):
    page = TestPage(base_url=url, driver=driver)
    page.check_caption()


def test_paragraphs(driver, url):
    page = TestPage(base_url=url, driver=driver)
    page.check_paragraphs()
