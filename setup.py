#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

setup(name='infoblox_axfr',
    version='0.1.0',
    description='InfoBlox axfr',
    author='Rob Tucker',
    author_email='rtucker@mozilla.com',
    packages=['infoblox_axfr'],
    setup_requires = [
        'dnspython==1.15'
    ],
    entry_points={
        'console_scripts': [
            'infoblox_axfr=infoblox_axfr.main:main'
        ],
    },
     )
