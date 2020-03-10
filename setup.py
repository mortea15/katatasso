#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Morten Amundsen'
__contact__ = 'm.amundsen@sportradar.com'

from setuptools import find_packages, setup

version = '0.0.1'
long_desc = '''katatasso -- a Machine Learning classifier for email.
'''.lstrip()

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Sportradar, NTNU',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Human Machine Interfaces',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Filters',
    'Topic :: Text Processing :: General',
    'Topic :: Text Processing :: Linguistic'
]

requires = [
    'scikit-learn',
    'tqdm'
]

setup(
    name='katatasso',
    version=version,
    description='A Machine Learning classifier for email',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    install_requires=requires,
    dependency_links=['git+ssh://git@github.com/mortea15/emailyzer.git'],
    url='https://github.com/mortea15/katatasso.git',
    author=__author__,
    author_email=__contact__,
    packages=['katatasso', 'katatasso.modules', 'katatasso.helpers', 'katatasso.tests'], #find_packages(),
    classifiers=classifiers,
    zip_safe=False,
    entry_points={'console_scripts': ['katatasso = katatasso.__main__:main']}
)
