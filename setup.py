from setuptools import setup
from setuptools.dist import Distribution
import Slash

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

__version__ = Slash.__version__

print(f"Slash version: {__version__}")

setup(
    name='Slash92',
    version=__version__,
    description='ORM',
    author='Telegram: @M_O_D_E_R',
    packages=['Slash', 'Slash/Core'],
    install_requires=['psycopg2'],
    include_package_data=True,
    distclass=BinaryDistribution,
    python_requires='>=3.8',
)

print("done...")