#!/usr/bin/env python

from distutils.core import setup

setup(
    name='backuptool',
    version='1.0',
    description='A backup utility',
    author='hvm',
    author_email='',
    url='https://github.com/hvm2hvm/backuptool',
    packages=['libbt'],
    requires=['django', 'pytest'],
)
