

"""
Setup script.

Use this script to install the pyOpenDial DM  module of the retico simulation framework.
Usage:
    $ python3 setup.py install
The run the simulation:
    $ retico [-h]
"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

config = {
    "description": "The pyOpenDial DM incremental module for the retico framework",
    "author": "Casey Kennington",
    "url": "??",
    "download_url": "??",
    "author_email": "caseykennington@boisestate.edu",
    "version": "0.1",
    "install_requires": ["retico-core~=0.2.0", "multipledispatch", "soundcard", "asteval", "PyQt5", "pyyaml==5.1.1"],
    "packages": find_packages(),
    "name": "retico-rasa-nlu",
}

setup(**config)