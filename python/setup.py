#!/usr/bin/env python3
"""
Setup script for GRASS DateTime Python wrapper
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "GRASS DateTime Library Python Wrapper"

setup(
    name="grass-datetime",
    version="1.0.0",
    author="GRASS DateTime Library Python Wrapper",
    description="Python wrapper for GRASS GIS DateTime library using CFFI",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/dudaka/grass_datetime_standalone",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "cffi>=1.15.0",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
        ],
    },
    keywords="datetime, grass, gis, cffi, time, date, timezone",
    project_urls={
        "Bug Reports": "https://github.com/dudaka/grass_datetime_standalone/issues",
        "Source": "https://github.com/dudaka/grass_datetime_standalone",
        "Documentation": "https://github.com/dudaka/grass_datetime_standalone/blob/main/python/README.md",
    },
)
