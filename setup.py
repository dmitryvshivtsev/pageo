from setuptools import setup, find_packages


with open("README.md", "r", encoding='utf-8') as readme_file:
    readme = readme_file.read()

__version__ = '0.1.3'

setup(
    name='pageo',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    description='Библиотека на базе Selenium с расширенным функционалом. Предназначена для работы с любым веб-сайтом и его страницами',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='dmitry',
    author_email='dmitryvshivtsev@gmail.com',
    install_requires=[
        'pytest>=7.4.0',
        'selenium>=4.10.0',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
    ],
)

