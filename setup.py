
from setuptools import setup, find_packages
import sys, os

version = '1.1'

setup(
    name = 'dm',
    version = version,
    description = "Dict to Data mapper",
    packages = find_packages( exclude = [ 'ez_setup'] ),
    include_package_data = True,
    zip_safe = False,
    entry_points = {},
    author = 'Bence Faludi',
    author_email = 'b.faludi@mito.hu',
    license = 'GPL',
    install_requires = [],
    test_suite = "dm.tests"
)
