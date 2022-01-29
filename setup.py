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
    long_description_content_type = "text/markdown",
    long_description=open('README.md', encoding="utf-8").read(),
    author='Telegram: @M_O_D_E_R',
    url="https://github.com/m-o-d-e-r/Slash",
    packages=['Slash', 'Slash/Core'],
    install_requires=['psycopg2'],
    platforms=["windows", "linux"],
    license="GPL-3.0",
    include_package_data=True,
    distclass=BinaryDistribution,
    python_requires='>=3.8',
)

print("done...")
