# pageo
[![Downloads](https://static.pepy.tech/badge/pageo)](https://pepy.tech/project/pageo)
[![Downloads](https://static.pepy.tech/badge/pageo/month)](https://pepy.tech/project/pageo)
[![lib-tests](https://github.com/dmitryvshivtsev/pageo/actions/workflows/test_package.yml/badge.svg)](https://github.com/dmitryvshivtsev/pageo/actions/workflows/test_package.yml)
[![PyPI version](https://badge.fury.io/py/pageo.svg)](https://badge.fury.io/py/pageo)
[![codecov](https://codecov.io/gh/dmitryvshivtsev/pageo/branch/develop/graph/badge.svg)](https://codecov.io/gh/dmitryvshivtsev/pageo)

<p align="center">
  <img src="https://github.com/dmitryvshivtsev/pageo/blob/main/docs/logo/pageo_logo.png?raw=true">
</p>

Библиотека на базе Selenium с расширенным функционалом. Предназначена для автоматической работы с любыми веб-страницами и их элементами. 
Вдохновлена [статьёй на Хабре](https://habr.com/ru/articles/472156/) и упрощает написание автоматических тестов 
с реализацией паттерна [PageObject](https://ru.wikipedia.org/wiki/PageObject). Ускорьте написание кода, а также сделайте его лаконичнее и яснее.

## Описание

Зачем нужна эта библиотека, если есть Selenium из коробки, который и предоставляет методы для работы со страницами веб-сайтов?
В процессе написания тестов, разработчик регулярно ищет элементы на странице, переходит на другие страницы,
получает аттрибуты и т.д.. Все это, как правило, оборачивается в ожидания, чтобы избежать внезапных ошибок.
Библиотека предоставляет базовый класс, методы которого позволяют скрыть часть этой логики, а также комбинируют в себе
различные инструменты базового Selenium, тем самым расширяя функциональность.
Благодаря этому ускоряется написание тестов, их понимание и последующая поддержка. 

Преимущества перед использованием Selenium из коробки:
- Простое использование путем наследования от базового класса в классы конкретных страниц.
- Возможность установить настройки для теста, просто передав их в аргументах класса страницы.
- Базовые [методы](#документация-базового-класса) поиска элементов расширены и включают в себя явное ожидание.
- [Классы локаторов](#классы-локаторов), скрывающие логику поиска элементов и возвращающие объект [`WebDriver`](https://www.selenium.dev/documentation/webdriver/drivers/service/).

##  Оглавление

- [Установка](#установка)
- [Быстрый старт](#быстрый-старт)
- [Документация базового класса](#документация-базового-класса)
  - [Создание объекта](#создание-объекта)
  - [Метод find_element](#метод-findelement)
  - [Метод find_elements](#метод-findelements)
  - [Метод custom_wait_until](#метод-customwaituntil)
  - [Метод move_to_element](#метод-movetoelement)
- [Классы локаторов](#классы-локаторов)
  - [class_name_locator](#classnamelocator)
  - [css_locator](#csslocator)
  - [id_locator](#idlocator)
  - [link_text_locator](#linktextlocator)
  - [name_locator](#namelocator)
  - [partial_link_text_locator](#partiallinktextlocator)
  - [tag_name_locator](#tagnamelocator)
  - [xpath_locator](#xpathlocator)
- [Использование в PageObject](#использование-в-pageobject)


## Установка

Установите core-page через pip:

```shell
pip install pageo
```

**Использование библиотеки подразумевает, что на вашем компьютере уже имеется chromedriver.
Если нет, то следует ознакомиться с [руководством](https://chromedriver.chromium.org/getting-started).**


## Быстрый старт:

Cоздаем файл для тестируемой страницы и импортируем класс BasePage.\
Создаем класс страницы и наследуемся от BasePage. Теперь нам доступны все [методы](#документация-класса) базового класса.
Также импортируем [класс локатора](#классы-локаторов) [`IdLocator`](#idlocator). С его помощью будет выполняться поиск элемента.

```python
# about_page.py

from pageo import BasePage
from pageo import IdLocator


class AboutPage(BasePage):
    search_field_element = IdLocator("id-search-field")

    def is_search_field(self):
        return True if self.search_field_element else False
```

Далее, можем создать экземпляр нашего класса `AboutPage` в тест-кейсе и передать необходимые [настройки](#создание-объекта).

```python
# test_about_page.py

from selenium import webdriver

from about_page import AboutPage


def test_search_field_exist():
    page = AboutPage(
        driver=webdriver.Chrome(),
        base_url='https://www.python.org',
        url_suffix='/about',
    )

    search_field_exist = page.is_search_field()
    print(page.is_search_field())
    assert search_field_exist
```
Подробнее этот пример описан в [разделе про Page Object](#использование-в-pageobject).

## Документация базового класса

### Создание объекта

Аттрибуты класса:
- **base_url** - адрес страницы без относительного пути. 
- **url_suffix** - **url_suffix** - относительный путь к конкретной странице сайта.
  > Адрес страницы может быть передан без протокола. В таком случае, будет установлен протокол по умолчанию (*https*).
  > Если адрес страницы имеет протокол *http*, то его следует указать перед адресом страницы самостоятельно!

Аргументы класса:
- **driver** - объект `WebDriver`. Обязательный аргумент.
- **base_url** - адрес страницы без относительного пути. 
  > - Передавайте URL в аргументах при создании объекта только в том случае, если адрес не был указан в аттрибутах класса страницы. 
  > - Если адрес страницы был указан и в аттрибутах класса, и в аргументах при создании объекта, но они отличаются, то будет выброшено исключение **UrlDisparityError**.
  > - Если URL не был указан ни в аттрибутах класса, ни в аргументах при создании объекта, то будет выброшено исключение **UrlAvailabilityError**.

  > Адрес страницы может быть передан без протокола. В таком случае, будет установлен протокол по умолчанию (*https*).
  > Если адрес страницы имеет протокол *http*, то его следует указать перед адресом страницы!

- **url_suffix** - относительный путь к конкретной странице сайта. По умолчанию относительный путь отсутствует.
  > - Передавайте относительный путь в аргументах при создании объекта только в том случае, если относительный путь к конкретной странице не был указан в аттрибутах класса страницы. 
  > - Если относительный путь был указан и в аттрибутах класса, и в аргументах при создании объекта, но они отличаются, то будет выброшено исключение **UrlDisparityError**.

- **window_size** - размер страницы браузера в формате `(ширина, высота)`. По умолчанию установлено значение (1920, 1080). 

**Рекомендуется предварительно создавать свой объект `WebDriver`.**\
Для примера создадим свой объект `WebDriver` и передадим ему опции:
```python
from selenium import webdriver
  
from main_page import MainPage
    
  
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
 
page = MainPage(driver=driver, base_url='https://google.com')
```

Можно передавать его непосредственно в класс (без предварительного создания):

```python
from selenium import webdriver
  
from main_page import MainPage


page = MainPage(driver=webdriver.Chrome(), base_url='https://google.com')
```

### Метод find_element

Метод `find_element` ищет элемент на странице по [локатору](https://www.selenium.dev/documentation/webdriver/elements/locators/) в течение определенного времени. Если элемент найден, то возвращает его.
Иначе выбрасывает TimeoutException.

Принимает следующие аргументы:
- by - [Стратегия для поиска элемента](https://www.selenium.dev/documentation/webdriver/elements/locators/). Обязательный аргумент.
- selector - [Селектор элемента, который необходимо найти](https://www.selenium.dev/documentation/webdriver/elements/finders/). Обязательный аргумент.
- duration - время в секундах, в течение которого будет осуществляться поиск элемента. Значение по умолчанию - 5 секунд.

```python
from selenium.webdriver.common.by import By

from page_objects import MainPage


def test_some_element():
    page = MainPage(base_url='https://google.com', url_suffix='/doodles')
      
    element = page.find_element(By.ID, 'about-link')
```

### Метод find_elements

Метод `find_element` ищет все элементы на странице по [локатору](https://www.selenium.dev/documentation/webdriver/elements/locators/) 
в течение определенного времени. Если элементы найдены, то возвращает список из этих элементов.
Иначе выбрасывает TimeoutException.

Принимает следующие аргументы:
- by - [Стратегия для поиска элементов](https://www.selenium.dev/documentation/webdriver/elements/locators/). Обязательный аргумент.
- selector - [Селектор элементов, которые необходимо найти](https://www.selenium.dev/documentation/webdriver/elements/finders/). Обязательный аргумент.
- duration - время в секундах, в течение которого будет осуществляться поиск элементов. Значение по умолчанию - 5 секунд.

```python
from selenium.webdriver.common.by import By

from page_objects import MainPage


def test_some_element():
    page = MainPage(base_url='https://google.com', url_suffix='/doodles')
  
    element = page.find_elements(By.ID, 'nav-list')
```

### Метод custom_wait_until

Метод `custom_wait_until` позволяет задавать ожидания на основе пользовательских условий. В случае, когда условие 
ожидания, которое нам нужно, не предусмотрено Selenium, пользователь может сам задать условие ожидания на основе какой-либо функции.

Принимает следующие аргументы:
- func_condition - функция предикат, в которой задано условие ожидания.
- duration - время в секундах, в течение которого будет выполняться ожидание.

```python
from selenium.webdriver.common.by import By

from page_objects import MainPage


def test_some_element():
    page = MainPage(base_url='https://google.com', url_suffix='/doodles')
  
    page.find_element(By.ID, 'about-link').click()
    page.custom_wait_until(lambda browser: browser.current_url != page.url)

    ...
```

### Метод move_to_element

Метод `move_to_element` имитирует наведение мыши на элемент. Комбинирует внутри себя создание объекта `ActionChains`, 
наведение на элемент и выполнение действия (метод perform).

Метод принимает один аргумент:
- element - объект `WebElement`, на который нужно выполнить наведение мыши.

```python
from selenium.webdriver.common.by import By

from page_objects import MainPage


def test_some_element():
    page = MainPage(base_url='https://google.com', url_suffix='/doodles')
  
    about_button = page.find_element(By.ID, 'about-link')
    page.move_to_element(about_button)
    
    ...
```

## Классы локаторов

Вспомогательные классы локаторов для `BasePage`, инкапсулирующие логику поиска элементов по локаторам.
Каждый класс наследуется от абстрактного класса `AbstractLocator`.
Использование классов локаторов позволяет объявлять их в классах страницы как аттрибуты класса. Если селектор изменится 
или нужно изменить стратегию поиска элемента, то достаточно просто изменить селектор элемента в аргументах класса или сам класс-стратегию.

Каждый класс локатора принимает следующие аргументы:
- selector - селектор искомого элемента. **Обязательный аргумент.**
- is_many - флаг, указывающий на множественность элементов. \
Если **False**, то будет возвращен один найденный элемент (первый элемент, который соответствует локатору). \
Если **True**, то будет возвращен список всех найденных элементов.
- timeout - время в секундах, в течение которого будет выполняться ожидание. По умолчанию 5 секунд.

Каждый класс локатора возвращает объект `WebElement`.

### class_name_locator

Класс локатора, выполняющий поиск на основе имени класса элемента.

```python
from pageo import BasePage
from pageo import ClassNameLocator 


class SomePage(BasePage):
    some_element = ClassNameLocator("some-class-name")

    ...
```

### css_locator

Класс локатора, выполняющий поиск на основе css-локатора элемента.

```python
from pageo import BasePage
from pageo import CSSLocator


class SomePage(BasePage):
    some_element = CSSLocator("some-css-locator")

    ...
```

### id_locator

Класс локатора, выполняющий поиск на основе аттрибута id у тега элемента.

```python
from pageo import BasePage
from pageo import IdLocator


class SomePage(BasePage):
    some_element = IdLocator("some-id-attribute")

    ...
```

### link_text_locator

Класс локатора, выполняющий поиск на основе текста внутри ссылки элемента.

```python
from pageo import BasePage
from pageo import LinkTextLocator


class SomePage(BasePage):
    some_element = LinkTextLocator("some-link-text")

    ...
```

### name_locator

Класс локатора, выполняющий поиск на основе аттрибута name у тега элемента.

```python
from pageo import BasePage
from pageo import NameLocator


class SomePage(BasePage):
    some_element = NameLocator("some-name-attribute")

    ...
```

### partial_link_text_locator

Класс локатора, выполняющий поиск на основе вхождения текста внутри ссылки элемента.

```python
from pageo import BasePage
from pageo import PartialLinkTextLocator


class SomePage(BasePage):
    some_element = PartialLinkTextLocator("some-partial-link-text")

    ...
```

### tag_name_locator

Класс локатора, выполняющий поиск на основе имени тега элемента.

```python
from pageo import BasePage
from pageo import TagNameLocator


class SomePage(BasePage):
    some_element = TagNameLocator("some-tag-name")

    ...
```

### xpath_locator

Класс локатора, выполняющий поиск на основе пути XPath до элемента.

```python
from pageo import BasePage
from pageo import XPATHLocator


class SomePage(BasePage):
    some_element = XPATHLocator("some-xpath")

    ...
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

Рассмотрим файл *about_page.py*. Он должен описывать методы, содержащие поиск элементов и взаимодействие с ними. \
В нашем случае, протестируем наличие поля для поиска по сайту.
Для поиска элемента на сайте будет использоваться `IdLocator`. 

```python
# about_page.py

from pageo import BasePage
from pageo import IdLocator

    
class AboutPage(BasePage):
    search_field_element = IdLocator("id-search-field")
    
    def is_search_field(self):
        return True if self.search_field_element else False
```

Перейдем в файл *test_about_page.py*. Здесь мы создаем тест-кейс, в котором проверяем сценарий, описанный в классе страницы.

```python
# test_about_page.py

from selenium import webdriver

from page_object.about_page import AboutPage


def test_search_field_exist():
  page = AboutPage(
      driver=webdriver.Chrome(),
      base_url='https://www.python.org', 
      url_suffix='/about', 
  )

  search_field_exist = page.is_search_field()
  assert search_field_exist
```

Благодаря такой структуре проекта и использованию паттерна, мы можем легко поддерживать и писать гибкие сценарии.
Даже при значительных изменениях тестируемой страницы, исправление тестов не займет много времени.
