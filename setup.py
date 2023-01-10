import io

from setuptools import setup, find_packages

version = "0.1.3"
requirements = ["requests==2.28.1"]

with io.open("README.rst", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="npyi",
    packages=find_packages(exclude=["test", "test.*"]),
    version=version,
    long_description=readme,
    description="API wrapper around the NPPES API",
    author="Andy Huynh",
    license="BSD",
    author_email="andy.huynh312@gmail.com",
    url="https://github.com/andyh1203/npyi",
    keywords=["npyi", "npi", "nppes"],
    install_requires=requirements,
)
