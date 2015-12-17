#!/usr/bin/env python

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup( name = "packagetex",
       version = "0.1",
       author = "Edward Smith",
       author_email = "edward.smith05@imperial.ac.uk",
       url = "https://github.com/edwardsmith999/packagetex",
       # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
       classifiers=['Development Status :: 3 - Alpha',
                     'Programming Language :: Python :: 2.7'],
       packages=find_packages(exclude=['contrib', 'docs', 'tests']),
       keywords='latex tarball package collaboration',
       license = "GPL",
       description = "Packages a tex file into a tarball with all figures",
       long_description = long_description,
       entry_points={
            'console_scripts': [
                'packagetex=packagetex:main',
            ],
       },
)
