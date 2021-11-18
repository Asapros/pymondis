from setuptools import setup


with open("README.md", encoding="utf-8") as readme_file:
    README = readme_file.read()

with open("requirements.txt", "r") as requirements_file:
    REQUIREMENTS = requirements_file.read().splitlines()

setup(
    name="pymondis",
    url="https://github.com/Asapros/pymondis",
    project_urls={
        "Tracker": "https://github.com/Asapros/pymondis/issues",
        "Source": "https://github.com/Asapros/pymondis"
    },
    version="1.0.0.a4",
    packages=("pymondis", "pymondis.abstract"),
    license="MIT",
    author="Asapros",
    description="Unofficial Quatromondis API wrapper",
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
