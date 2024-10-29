from setuptools import setup, find_packages

setup(
    name='atc_tracker',
    version='0.1.0',
    description='The Air traffic Control in your terminal',
    author='Luckyluka17',
    packages=find_packages(),
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
)
