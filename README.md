<div align="center">

<img src="https://raw.githubusercontent.com/Luckyluka17/atc_tracker/refs/heads/main/assets/images/banner2.png" width="500px" alt="logo">

![GitHub Repo stars](https://img.shields.io/github/stars/Luckyluka17/atc_tracker?style=flat&logo=github&label=Github%20stars)
![PyPI - Version](https://img.shields.io/pypi/v/atc_tracker?logo=pypi&label=Latest%20version)
![PyPI - Downloads](https://img.shields.io/pypi/dd/atc-tracker?logo=pypi&label=Daily%20downloads)
![PyPI - Downloads](https://img.shields.io/pypi/dm/atc-tracker?logo=pypi&label=Monthly%20downloads)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Luckyluka17/atc_tracker/python-publish.yml?logo=python&logoColor=white&label=Build%20status)

</div>


## Features
- Display of all current flights
- ETA calculation using precise aircraft and arrival airport coordinates
- Advanced search with combinable filters (Search by airline, model, registration, etc.)
- Real-time flight tracking with full flight details
- Detailed airport information

## Screenshots

<details>
<summary>Airport details</summary>

![Airport details](https://raw.githubusercontent.com/Luckyluka17/atc_tracker/main/assets/images/overview/image.png)

</details>

<details>
<summary>Flights list (with filters)</summary>

![Flights list (with filters)](https://raw.githubusercontent.com/Luckyluka17/atc_tracker/main/assets/images/overview/image2.png)

</details>


## Installation

### From PyPi

```
pip install atc_tracker
```

### From source (Github)

```
git clone https://github.com/Luckyluka17/atc_tracker.git
cd atc_tracker/
python setup.py install
```

## Build

```
pip install build 
python -m build
twine check dist/* # Checking the build
```
