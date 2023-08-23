from setuptools import setup


with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name='core_page',
    version='0.0.1',
    packages=['base_page'],
    description='Утилита для расширенного взаимодействия с любым веб-сайтом и его страницами',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='dmitry',
    author_email='dmitryvshivtsev@gmail.com',
    install_requires=[
        'pytest==7.4.0',
        'selenium==4.10.0',
    ],
)

