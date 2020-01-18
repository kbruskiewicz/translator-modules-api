# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "cwl_server"
VERSION = "0.0.1"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion==2.0.0",
    "swagger-ui-bundle==0.0.2",
    "python_dateutil==2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="NCATS Workflow Runner",
    author_email="kenneth@starinformatics.com",
    url="https://github.com/ncats/translator-modules/master/cwl_server",
    keywords=["OpenAPI", "NCATS Workflow Runner"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['cwl_server=cwl_server.__main__:main']},
    long_description="""\
    executes and creates multi-step, multi-input, scatterable workflows that chain together scripts from Translator Modules
    """
)

