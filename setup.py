from setuptools import setup


setup(
    name="Flagsmith Flag Engine",
    version="0.1.0",
    author="Matthew Elwell",
    author_email="matthew.elwell@flagsmith.com",
    packages=["flag_engine"],
    url="http://pypi.python.org/pypi/flagsmith-flag-engine/",
    license="LICENSE.txt",
    description="Flag engine for the Flagsmith API.",
    long_description=open("README.md").read(),
    install_requires=["marshmallow", "dataclasses"],
)
