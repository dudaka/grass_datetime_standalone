"""
GRASS DateTime Python Package

A Python interface to the GRASS DateTime C library.
"""

from .grass_datetime import (
    DateTime,
    DateTimeError,
    days_in_month,
    is_leap_year,
    days_in_year,
    ABSOLUTE,
    RELATIVE,
    YEAR,
    MONTH,
    DAY,
    HOUR,
    MINUTE,
    SECOND
)

__version__ = "1.0.0"
__author__ = "GRASS DateTime Python Wrapper"

__all__ = [
    'DateTime',
    'DateTimeError',
    'days_in_month',
    'is_leap_year',
    'days_in_year',
    'ABSOLUTE',
    'RELATIVE',
    'YEAR',
    'MONTH',
    'DAY',
    'HOUR',
    'MINUTE',
    'SECOND'
]
