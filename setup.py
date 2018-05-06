import os
from distutils.core import setup

setup(
    name = "JXMonitor",
    version = "0.1-alpha",
    author = "Jason Xie",
    author_email = "jason.xie@victheme.com",
    description = "Python script for monitoring JXMiner via TUI",
    packages=['jxmonitor', 'jxmonitor.threads', 'jxmonitor.modules', 'jxmonitor.widgets', 'jxmonitor.entities'],
    package_dir={'jxmonitor': 'src'},
    entry_points = {
        'console_scripts' : ['jxmonitor = jxmonitor.jxmonitor:main']
    },
)