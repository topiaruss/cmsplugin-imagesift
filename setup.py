#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import imagesift

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = imagesift.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='cmsplugin-imagesift',
    version=version,
    description="""A django-CMS gallery that dynamically selects images from imagestore.""",
    long_description=readme + '\n\n' + history,
    author='Russ Ferriday',
    author_email='russf@topia.com',
    url='https://github.com/topiaruss/cmsplugin-imagesift',
    packages=[
        'imagesift',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='cmsplugin-imagesift',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)