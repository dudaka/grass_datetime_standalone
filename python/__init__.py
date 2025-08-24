"""
GRASS DateTime Library Python Wrapper

A comprehensive Python wrapper for the GRASS DateTime library using CFFI.
"""

from .grass_datetime import (
    DateTime,
    DateTimeError,
    days_in_month,
    is_leap_year,
    days_in_year,
    DATETIME_ABSOLUTE,
    DATETIME_RELATIVE,
    DATETIME_YEAR,
    DATETIME_MONTH,
    DATETIME_DAY,
    DATETIME_HOUR,
    DATETIME_MINUTE,
    DATETIME_SECOND,
)

__version__ = "1.0.0"
__author__ = "GRASS DateTime Library Python Wrapper"
__description__ = "Python wrapper for GRASS GIS DateTime library using CFFI"

__all__ = [
    "DateTime",
    "DateTimeError",
    "days_in_month",
    "is_leap_year", 
    "days_in_year",
    "DATETIME_ABSOLUTE",
    "DATETIME_RELATIVE",
    "DATETIME_YEAR",
    "DATETIME_MONTH",
    "DATETIME_DAY",
    "DATETIME_HOUR",
    "DATETIME_MINUTE",
    "DATETIME_SECOND",
]
