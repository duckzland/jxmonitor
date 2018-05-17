from setuptools import setup, find_packages
setup(
    name = "JXMonitor",
    version = "0.1-alpha",
    author = "Jason Xie",
    author_email = "jason.xie@victheme.com",
    description = "Python script for monitoring JXMiner via TUI",
    packages=find_packages('src'),
    package_dir={'':'src'},
    include_package_data=True,
    install_requires=['urwid'],
    entry_points = {
        'console_scripts' : ['jxmonitor = jxmonitor.jxmonitor:main']
    },
)