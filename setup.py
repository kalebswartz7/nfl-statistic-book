#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['requests']

python_requires='>3',

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Kaleb Swartz",
    author_email='kalebswartz7@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Python application that retrieves information from MySportsFeed API based on NFL teams",
    entry_points={
        'console_scripts': [
            'nfl_statistic_book=nfl_statistic_book.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nfl_statistic_book',
    name='nfl_statistic_book',
    packages=find_packages(include=['nfl-statistic-book']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kalebswartz7/nfl-statistic-book',
    version='1.0.1',
    zip_safe=False,
)
