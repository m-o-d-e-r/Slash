import os
from setuptools import setup
from setuptools.dist import Distribution

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

__version__ = "1.0"

setup(
    name='Slash',
    version=__version__,
    description='ORM',
    author='Telegram: @M_O_D_E_R',
    packages=['Slash', 'Slash/Core'],
    install_requires=['psycopg2'],
    include_package_data=True,
    distclass=BinaryDistribution,
)