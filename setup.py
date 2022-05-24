from setuptools import find_packages, setup

setup(
    name="flagsmith-flag-engine",
    version="2.0.6",
    author="Flagsmith",
    author_email="support@flagsmith.com",
    packages=find_packages(include=["flag_engine", "flag_engine.*"]),
    url="https://github.com/Flagsmith/flagsmith-engine",
    license="BSD3",
    description="Flag engine for the Flagsmith API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "marshmallow>=3.14.1",
        "dataclasses;python_version<'3.7'",
        "semver==2.13.0",
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
