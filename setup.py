from setuptools import find_packages, setup

setup(
    name="flagsmith-flag-engine",
    version="4.1.0",
    author="Flagsmith",
    author_email="support@flagsmith.com",
    packages=find_packages(include=["flag_engine", "flag_engine.*"]),
    url="https://github.com/Flagsmith/flagsmith-engine",
    license="BSD3",
    description="Flag engine for the Flagsmith API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "pydantic>=1.10.8,<2",
        "pydantic-collections>=0.4.0,<1",
        "semver==2.13.0",
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
