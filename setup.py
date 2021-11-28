from setuptools import setup
from .pymondis import __version__, __license__, __description__, __title__, __author__

with open("README.md", encoding="utf-8") as readme_file:
    README = readme_file.read()

with open("requirements.txt", "r") as requirements_file:
    REQUIREMENTS = requirements_file.read().splitlines()

setup(
    name=__title__,
    url="https://github.com/Asapros/pymondis",
    project_urls={
        "Tracker": "https://github.com/Asapros/pymondis/issues",
        "Source": "https://github.com/Asapros/pymondis"
    },
    version=__version__,
    packages=("pymondis",),
    license=__license__,
    author=__author__,
    description=__description__,
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=REQUIREMENTS,
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: Polish",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers"
    ],
    keywords=("quatromondis", "yorck", "API", "HTTP", "async", "hugo")
)
