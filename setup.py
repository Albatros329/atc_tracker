from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

version_file = Path(__file__).parent / "atc_tracker" / "__version__.py"
version_globals = {}
with open(version_file) as f:
    exec(f.read(), version_globals)
VERSION = version_globals['__version__']

setup(
    name='atc_tracker',
    version=VERSION,
    description='The Air traffic Control in your terminal',
    author='Luckyluka17',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'atc_tracker=atc_tracker.main:main',
        ],
    },
    install_requires=[
        "colorama",
        "FlightRadarAPI",
        "pynput",
        "pytz",
        "keyboard",
        "setuptools"
    ],
    python_requires='>=3.10',
    url="https://github.com/Luckyluka17/atc_tracker/"
)
