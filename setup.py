from setuptools import setup, find_packages

NAME = "crossengage-client"
VERSION = "1.1.1"

REQUIRES = []

setup(
    name=NAME,
    version=VERSION,
    description="Crossengage Python Client",
    author_email="azh@hellofresh.com",
    keywords=["HelloFresh", "Crossengage", "CRM"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=('tests',)),
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ],
)
