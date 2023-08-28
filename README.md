# core-page
[![lib-tests](https://github.com/dmitryvshivtsev/core_page/actions/workflows/test_package.yml/badge.svg)](https://github.com/dmitryvshivtsev/core_page/actions/workflows/test_package.yml)
[![PyPI version](https://badge.fury.io/py/core-page.svg)](https://badge.fury.io/py/core-page)
[![codecov](https://codecov.io/gh/dmitryvshivtsev/core_page/branch/develop/graph/badge.svg)](https://codecov.io/gh/dmitryvshivtsev/core_page)

<p align="center">
  <img src="logo/logo.png">
</p>

Библиотека для автоматической работы с любыми веб-страницами и их элементами на базе Selenium. 
Вдохновлена статьёй на [Хабр](https://habr.com/ru/articles/472156/) и упрощает написание автоматических тестов 
с реализацией паттерна [PageObject](https://ru.wikipedia.org/wiki/PageObject). Ускорьте написание кода, а также сделайте его лаконичнее и яснее.

## Описание

Зачем нужна эта библиотека, если есть Selenium из коробки, который и предоставляет методы для работы со страницами веб-сайтов?
В процессе написания тестов, разработчик регулярно ищет элементы на странице, переходит на другие страницы,
получает аттрибуты и т.д.. Все это, как правило, оборачивается в ожидания, чтобы избежать внезапных ошибок.
Библиотека предоставляет базовый класс, методы которого позволяют скрыть часть этой логики, а также комбинируют в себе
различные инструменты базового Selenium, тем самым расширяя функциональность.
Благодаря этому, ускоряется написание тестов, их понимание и последующая поддержка. 

Преимущества перед использованием Selenium из коробки:
- Простое использование, путем наследования от базового класса в классы конкретных страниц.
- Возможность установить настройки для теста, просто передав их в аргументах класса.
- Базовые методы поиска элементов расширены и включают в себя явное ожидание.

##  Оглавление

* [Установка](#)
* [Быстрый старт](#быстрый-старт)
* [Документация класса](#документация-класса)
    * [Создание объекта](#создание-объекта)
    * [Метод go_to_site](#метод-gotosite)
    * [Метод find_element](#метод-findelement)
    * [Метод find_elements](#метод-findelements)
    * [Метод custom_wait_until](#метод-customwaituntil)
    * [Метод move_to_element](#метод-movetoelement)
* [Использование в PageObject](#использование-в-pageobject)


## Установка

Установите core-page через pip:

```shell
pip install core-page
```

**Использование библиотеки подразумевает, что на вашем компьютере уже имеется chromedriver.
Если нет, то следует ознакомиться с [руководством](https://chromedriver.chromium.org/getting-started).**


## Быстрый старт:

Cоздаем файл для тестируемой страницы и импортируем класс BasePage.\
Создаем класс страницы и наследуемся от BasePage. Теперь нам доступны все [методы](#документация-класса) базового класса.

```python
# main_page.py

from base_page.base_page import BasePage

class MainPage(BasePage):
    pass
```

Далее, можем создать экземпляр нашего класса MainPage в тест-кейсе и передать необходимые [настройки](#создание-объекта).

```python
# test_main_page.py

from page_objects import MainPage


def test_main_page_title():
    page = MainPage(base_url='https://example.com', window_size=(1366, 768))
    
    page.go_to_site()
    
    ...
```
С более подробным примером можно ознакомится в [разделе про Page Object](#использование-в-pageobject).

## Документация класса

### Создание объекта

Все возможные аргументы класса:
- **driver** - объект WebDriver.
- **driver_fabric** - класс WebDriver.
- **base_url** - адрес страницы без относительного пути. 
**Перед адресом страницы должен быть указан протокол!** \
Пример: `https://google.com`
- **window_size** - размер страницы браузера в формате `(ширина, высота)`. По умолчанию установлено значение (1920, 1080).
- **url_suffix** - относительный путь к конкретной странице сайта. По умолчанию относительный путь отсутствует.


При создании объекта есть два варианта:
* Без передачи собственного драйвера. В этом случае драйвер создается в конструкторе. 
  ```python
  page = MainPage(base_url='https://google.com')
  ```
  
  Обязательные аргументы:
  - base_url;

  Необязательные аргументы:
  - driver_fabric;
  - window_size;
  - url_suffix;
  
  >   По умолчанию будет создан драйвер для Chrome без опций. Если хотите использовать свой объект WebDriver, 
  >   то воспользуйтесь следующим вариантом. 

* С передачей собственного объекта WebDriver. \
  Для примера создадим свой объект WebDriver и передадим ему опции:
    ```python
    from selenium import webdriver
    
  
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
 
    page = MainPage.with_driver(driver=driver, base_url='https://google.com')
    ```
Обязательные аргументы:
  - driver;
  - base_url;

  Необязательные аргументы:
  - window_size;
  - url_suffix;

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

### Метод custom_wait_until

Метод `custom_wait_until` позволяет задавать ожидания на основе пользовательских условий. В случае, когда условие 
ожидания, которое нам нужно, не предусмотрено Selenium, пользователь может сам задать условие ожидания на основе какой-либо функции.

Принимает следующие аргументы:
- func_condition - функция предикат, в которой задано условие ожидания.
- duration - время в секундах, в течение которого будет выполняться ожидание.

```python
from page_objects import MainPage


def test_some_element():
    page = MainPage(base_url='https://google.com', url_suffix='/doodles')

    page.go_to_site()
    
    some_link = page.find_element(locator).click()
    page.custom_wait_until(lambda browser: browser.current_url != page.url)
```

### Метод move_to_element

Метод `move_to_element` имитирует наведение мыши на элемент. Комбинирует внутри себя создание объекта *ActionChains*, 
наведение на элемент и выполнение действия (метод perform).

Метод принимает один аргумент:
- element - объект **WebElement**, на который нужно выполнить наведение мыши. 

```python
from page_objects import MainPage


def test_some_element():
    page = MainPage(base_url='https://google.com', url_suffix='/doodles')

    page.go_to_site()
    
    dropdown_menu = page.find_element(locator)
    page.move_to_element(dropdown_menu)
    
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
Над классом страницы можно описать класс, содержащий локаторы элементов на странице.
В нашем случае, протестируем наличие поля для поиска по сайту.

```python
# about_page.py

from base_page.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class AboutPageLocators:
    LOCATOR_SEARCH_FIELD = (By.ID, "id-search-field")

    
class AboutPage(BasePage):
    def is_search_field(self):
        try:
          self.find_element(AboutPageLocators.LOCATOR_SEARCH_FIELD)
          return True
        except TimeoutException:
          return False
```

Перейдем в файл *test_about_page.py*. Здесь мы создаем тест-кейс, в котором проверяем сценарий, описанный в классе страницы.

```python
# test_about_page.py

from page_object.about_page import AboutPage


def test_search_field_exist():
    page = AboutPage(base_url='https://www.python.org',
                     url_suffix='/about',)
    
    page.go_to_site()
    search_field_exist = page.is_search_field()
    assert search_field_exist
```

Благодаря такой структуре проекта и использованию паттерна, мы можем легко поддерживать и писать гибкие сценарии.
Даже при значительных изменениях тестируемой страницы, исправление тестов не займет много времени.
