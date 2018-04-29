# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='SmartMusroomHouse',
    version='0.1.0',
    description='Mushroom House Automation',
    long_description=readme,
    author='TrungCaoSy',
    author_email='caotrung.kk@gmail.com',
    url='https://github.com/caosytrung/SmartMushroomHouse',
    packages=find_packages(exclude=('tests', 'docs'))
)