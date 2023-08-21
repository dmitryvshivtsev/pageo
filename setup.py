from setuptools import setup

setup(
    name='core_page',
    version='0.1',
    packages=['core_page'],
    description='Утилита для взаимодействия с любым веб-сайтом и его страницами',
    author='dmitry',
    author_email='dmitryvshivtsev@gmail.com',
    install_requires=[
        'pytest==7.4.0',
        'selenium==4.10.0',
    ],
)


