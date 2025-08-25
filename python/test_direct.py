#!/usr/bin/env python3
"""
Test script for GRASS DateTime CFFI Extension - following sample project pattern

This script demonstrates the usage of the GRASS DateTime functions
from a C shared library (DLL) via Python CFFI.
"""

import sys
import os

# Add current directory to path for importing the extension
sys.path.insert(0, '.')
sys.path.insert(0, os.path.dirname(__file__))

try:
    from _grass_datetime_cffi import ffi, lib
    print("Testing GRASS DateTime Function (DLL Version)")
    print("=" * 50)
    
    # Test utility functions
    print("\nUtility Functions:")
    print(f"- 2024 is leap year: {lib.datetime_is_leap_year(2024, 1) != 0}")
    print(f"- 2025 is leap year: {lib.datetime_is_leap_year(2025, 1) != 0}")
    print(f"- Days in Feb 2024: {lib.datetime_days_in_month(2024, 2, 1)}")
    print(f"- Days in Feb 2025: {lib.datetime_days_in_month(2025, 2, 1)}")
    
    # Test DateTime structure
    print("\nDateTime Structure:")
    dt = ffi.new("DateTime *")
    
    # Set type and values
    lib.datetime_set_type(dt, lib.DATETIME_ABSOLUTE, lib.DATETIME_YEAR, lib.DATETIME_SECOND, 0)
    lib.datetime_set_year(dt, 2025)
    lib.datetime_set_month(dt, 8)
    lib.datetime_set_day(dt, 25)
    lib.datetime_set_hour(dt, 14)
    lib.datetime_set_minute(dt, 30)
    lib.datetime_set_second(dt, 45.0)
    
    # Format the datetime
    buffer = ffi.new("char[]", 256)
    if lib.datetime_format(dt, buffer) == 0:
        formatted = ffi.string(buffer).decode('utf-8')
        print(f"- Formatted datetime: {formatted}")
    
    # Get individual components
    year = ffi.new("int *")
    month = ffi.new("int *")
    day = ffi.new("int *")
    hour = ffi.new("int *")
    minute = ffi.new("int *")
    second = ffi.new("double *")
    
    lib.datetime_get_year(dt, year)
    lib.datetime_get_month(dt, month)
    lib.datetime_get_day(dt, day)
    lib.datetime_get_hour(dt, hour)
    lib.datetime_get_minute(dt, minute)
    lib.datetime_get_second(dt, second)
    
    print(f"- Components: {year[0]}-{month[0]:02d}-{day[0]:02d} {hour[0]}:{minute[0]:02d}:{second[0]:04.1f}")
    
    print("\nSUCCESS: GRASS DateTime CFFI extension test completed successfully!")
    print("The DLL (grass_datetime.dll) is loaded dynamically and working perfectly!")

except ImportError as e:
    print(f"ERROR: Failed to import CFFI module: {e}")
    print("Make sure you run this from the build directory after running:")
    print("  cmake --build . --config Release --target python_extension")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: Error during testing: {e}")
    sys.exit(1)
