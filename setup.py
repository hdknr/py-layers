#! /usr/bin/env python
from setuptools import setup, find_packages
from glob import glob

NAME = 'py-layers'
DESCRIPTION = 'Layers library and commands'
URL = 'https://github.com/hdknr/' + NAME
SCRIPTS = glob('scripts/*.py')
PACKAGES = [
    i for i in find_packages(exclude=['scripts', 'docs'])
    if '.' not in i]

VERSION = getattr(__import__(PACKAGES[0]),  '__version__')
REQUIRES = [
    i.strip() for i in
    open('requirements/pypi.txt').readlines() if i[0] != '#']
README = open('README.md').read()
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Simplifed BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.7',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


setup(
    license='Simplfied BSD License',
    author='Hideki Nara of LaFoaglia,Inc.',
    author_email='gmail [at] hdknr.com',
    maintainer='LaFoglia,Inc.',
    maintainer_email='gmail [at] hdknr.com',
    classifiers=CLASSIFIERS,
    name=NAME,
    version=VERSION,
    url=URL,
    description=DESCRIPTION,
    download_url=URL,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    long_description=README,
    scripts=SCRIPTS,
    install_requires=REQUIRES,
)