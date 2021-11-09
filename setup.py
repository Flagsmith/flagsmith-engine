from setuptools import find_packages, setup

setup(
    name="Flagsmith Flag Engine",
    version="0.1.1",
    author="Matthew Elwell",
    author_email="matthew.elwell@flagsmith.com",
    packages=find_packages(include=["flag_engine", "flag_engine.*"]),
    url="http://pypi.python.org/pypi/flagsmith-flag-engine/",
    license="LICENSE.txt",
    description="Flag engine for the Flagsmith API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["marshmallow", "dataclasses"],
)
