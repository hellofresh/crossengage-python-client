from setuptools import setup, find_packages

NAME = "crossengage-client"
VERSION = "0.5.0"

REQUIRES = []

setup(
    name=NAME,
    version=VERSION,
    description="Crossengage python client",
    author_email="azh@hellofresh.com",
    keywords=["HelloFresh", "Crossengage", "CRM"],
    install_requires=REQUIRES,
    packages=find_packages()
)
