from setuptools import setup


with open("README.md", "r", encoding='utf-8') as readme_file:
    readme = readme_file.read()

__version__ = '0.1.0'

setup(
    name='pageo',
    version=__version__,
    packages=['pageo'],
    description='Библиотека на базе Selenium с расширенным функционалом. Предназначена для работы с любым веб-сайтом и его страницами',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='dmitry',
    author_email='dmitryvshivtsev@gmail.com',
    install_requires=[
        'pytest>=7.4.0',
        'selenium>=4.10.0',
    ],
)

