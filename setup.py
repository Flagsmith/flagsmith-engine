from setuptools import find_packages, setup

setup(
    name="flagsmith-flag-engine",
    version="9.1.0",
    author="Flagsmith",
    author_email="support@flagsmith.com",
    packages=find_packages(include=["flag_engine", "flag_engine.*"]),
    package_data={"flag_engine": ["py.typed"]},
    url="https://github.com/Flagsmith/flagsmith-engine",
    license="BSD3",
    description="Flag engine for the Flagsmith API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "jsonpath-rfc9535>=0.1.5,<1",
        "semver>=3.0.4,<4",
        "typing-extensions>=4.14.1,<5",
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
