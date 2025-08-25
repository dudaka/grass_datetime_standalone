"""
Setup script for GRASS DateTime Python bindings
"""

from setuptools import setup, find_packages
import os

# Get the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read the README file
readme_path = os.path.join(os.path.dirname(script_dir), 'README.md')
with open(readme_path, 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="grass-datetime",
    version="1.0.0",
    description="Python bindings for GRASS DateTime C library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="GRASS Development Team",
    author_email="grass-dev@lists.osgeo.org",
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
        "cffi>=1.12.0",
    ],
    setup_requires=[
        "cffi>=1.12.0",
    ],
    cffi_modules=["grass_datetime_build.py:ffi"],
    include_package_data=True,
    zip_safe=False,
)
