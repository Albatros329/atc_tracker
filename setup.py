from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='atc_tracker',
    version='0.1.2-beta',
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
        "keyboard",
        "pytz",
        "setuptools"
    ],
    python_requires='>=3.10'
)
