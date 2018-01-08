#from distutils.core import setup
# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = myproject.settings']},
    install_requires = [],
    include_package_data = True
)
