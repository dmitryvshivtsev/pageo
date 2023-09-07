from urllib.parse import urljoin


def get_base_url_with_protocol(base_url: str) -> str:
    """
    Метод добавляет к базовому адресу протокол https, если протокол отсутствует.
    """
    return urljoin('https://', base_url) \
        if not base_url.startswith('https://') and not base_url.startswith('http://') \
        else base_url
