#!/usr/bin/env python

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='celery-dedupe',
    version='0.0.1',
    description='Deduplication of Celery tasks',
    author='Joe Alcorn',
    author_email='joealcorn123@gmail.com',
    url='https://github.com/joealcorn/celery-dedupe',
    packages=find_packages(),
    package_data={
        'celery_dedupe': ['README.md'],
    },
    long_description=readme,
    license='MIT',
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
