# core-page
[![lib-tests](https://github.com/dmitryvshivtsev/core_page/actions/workflows/test_package.yml/badge.svg)](https://github.com/dmitryvshivtsev/core_page/actions/workflows/test_package.yml)
[![lib-publish](https://github.com/dmitryvshivtsev/core_page/actions/workflows/publish_package.yml/badge.svg)](https://github.com/dmitryvshivtsev/core_page/actions/workflows/publish_package.yml)

Библиотека для автоматической работы с любыми веб-страницами и их элементами на базе Selenium. 
Вдохновлена статьёй на [Хабр](https://habr.com/ru/articles/472156/) и упрощает написание автоматических тестов 
с реализацией паттерна [PageObject](https://ru.wikipedia.org/wiki/PageObject). Ускорьте написание кода, а также сделайте его лаконичнее, яснее и гибче.

## Описание

Есть Selenium из коробки, который и предоставляет методы для работы со страницами. Зачем нужна эта библиотека?
В процессе написания тестов, разработчик регулярно ищет элементы на странице, переходит на другие страницы,
получает аттрибуты и т.д.. Все это, как правило, оборачивается в ожидания, чтобы избежать внезапных ошибок.
Библиотека позволяет скрыть часть логики, а также комбинирует различные инструменты в отдельные методы.
Благодаря этому, ускоряется написание тестов, их понимание и последующая поддержка. 

Преимущества перед использованием Selenium из коробки:
- Простое использование, путем наследования от базового класса в классы конкретных страниц.
- Возможность установить настройки для теста, просто передав их в аргументах класса.
- Базовые методы поиска элементов расширены и включают в себя явное ожидание.
- Методы для получения аттрибутов у любого элемента. Просто передайте локатор.
- Скачивание изображений и возможность их проверки.

##  Оглавление

* [Быстрый старт](#быстрый-старт)
* [Документация класса](#документация-класса)
    * [Chromedriver](#chromedriver) 
    * [Конструктор класса](#конструктор-класса)
    * [Метод go_to_site](#метод-gotosite)
    * [Метод find_element](#метод-findelement)
    * [Метод find_elements](#метод-findelements)
* [Использование в PageObject](#использование-в-pageobject)


## Быстрый старт:

Установите core-page через pip:

```shell
pip install core-page
```

Далее, создаем файл для тестируемой страницы и импортируем класс BasePage.\
Создаем класс и наследуемся от BasePage. Теперь нам доступны все [методы](#документация-класса) базового класса.

```python
# main_page.py

from base_page.base_page import BasePage

class MainPage(BasePage):
    def get_title(self):
        return self.find_element(locator).text

    ...
```

Далее, можем создать экземпляр нашего класса MainPage в тест-кейсе и передать необходимые [настройки](#конструктор-класса).

```python
# test_main_page.py

from page_objects import MainPage


def test_main_page_title(driver):
    page = MainPage(driver=driver,
                    base_url='https://example.com',
                    url_suffix='',)
    
    page.go_to_site()
    
    ...
```

## Документация класса

### Chromedriver

Использование библиотеки подразумевает, что в вашем окружении уже установлен [chromedriver](https://chromedriver.chromium.org/getting-started).
Если нет, то следует ознакомиться с [руководством](https://chromedriver.chromium.org/getting-started).

### Конструктор класса

Конструктор класса BasePage позволяет установить следующие настройки:
- **driver - драйвер для работы браузером.** По умолчанию создаёт драйвер для Chrome, если не был передан иной драйвер;
- **base_url - адрес страницы без относительного пути.** По умолчанию получает содержимое переменной 'BASE_URL' из окружения. 
Если планируется работать лишь с одной страницей, то добавьте адрес страницы в окружение. 
**Перед адресом страницы должен быть указан протокол!** \
Пример: `https://google.com`
- **window_size** - размер страницы браузера в формате `(высота, ширина)`. По умолчанию установлено значение (1920, 1080).
- **url_suffix** - относительный путь к конкретной странице сайта. По умолчанию относительный путь отсутствует.


### Метод go_to_site

Осуществляет переход по полному URL страницы (после объединения **base_url** и **url_suffix**). 
Метод `go_to_site` ничего не принимает и не возвращает.

```python
from page_objects import MainPage


def test_some_element():
    page = MainPage(base_url='https://google.com', url_suffix='/doodles')
    
    page.go_to_site()  # Переход на сайт https://google.com/doodles
```

### Метод find_element

Метод `find_element` ищет элемент на странице по [локатору](https://www.selenium.dev/documentation/webdriver/elements/locators/) в течение определенного времени. Если элемент найден, то возвращает его.
Иначе выбрасывает TimeoutException.

Принимает следующие аргументы:
- locator - [локатор](https://www.selenium.dev/documentation/webdriver/elements/locators/) элемента. Значения по умолчанию нет.
- duration - время в секундах, в течение которого будет осуществляться поиск элемента. Значение по умолчанию - 5 секунд.

```python
from page_objects import MainPage


def test_some_element():
    page = MainPage(base_url='https://google.com', url_suffix='/doodles')
    
    page.go_to_site()
    element = page.find_element(locator, duration=10)
```

### Метод find_elements

Метод `find_element` ищет все элементы на странице по [локатору](https://www.selenium.dev/documentation/webdriver/elements/locators/) 
в течение определенного времени. Если элементы найдены, то возвращает список из этих элементов.
Иначе выбрасывает TimeoutException.

Принимает следующие аргументы:
- locator - [локатор](https://www.selenium.dev/documentation/webdriver/elements/locators/) элементов. Значения по умолчанию нет.
- duration - время в секундах, в течение которого будет осуществляться поиск элементов. Значение по умолчанию - 5 секунд.

```python
from page_objects import MainPage


def test_some_element():
    page = MainPage(base_url='https://google.com', url_suffix='/doodles')
    
    page.go_to_site()
    element = page.find_elements(locator)
```

## Использование в [PageObject](https://ru.wikipedia.org/wiki/PageObject)

Использование паттерна [PageObject](https://ru.wikipedia.org/wiki/PageObject) позволяет упростить написание, поддержку 
и масштабирование тестов. Базовый класс может в этом помочь. 

Допустим, нужно протестировать сайт `https://www.python.org/`. Он содержит множество страниц и элементов.
Паттерн подразумевает, что каждая страница будет представлена как отдельный класс с методами страницы.

В таком случае, структура проекта может выглядеть следующим образом:
```
project/
├── page_object/
│   ├── __init__.py
│   ├── main_page.py
│   └── about_page.py
├── tests/
│   ├── __init__.py
│   ├── test_main_page.py
│   └── test_about_page.py
├── ...
└── ...
```



