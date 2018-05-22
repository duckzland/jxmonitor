#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "jxmonitor",
    version = "0.2-alpha",
    author = "Jason Xie",
    author_email = "jason.xie@victheme.com",
    description = "Python script for monitoring JXMiner via TUI",
    packages=['jxmonitor', 'jxmonitor.modules', 'jxmonitor.threads', 'jxmonitor.widgets', 'jxmonitor.entities'],
    package_dir={'jxmonitor' : 'jxmonitor'},
    include_package_data=True,
    install_requires=[
        'urwid',
        'setuptools'
    ],
    entry_points = {
        'console_scripts' : ['jxmonitor = jxmonitor.jxmonitor:main']
    },
)