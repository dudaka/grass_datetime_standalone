#!/usr/bin/env python3
"""
GRASS DateTime Python bindings example using os.add_dll_directory()
This demonstrates how to use the CFFI bindings without copying the DLL
to the same directory as the Python extension.
"""

import os
import sys

# Add the DLL directory to Python's DLL search path (Python 3.8+)
dll_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'build', 'Release'))
if os.path.exists(dll_directory):
    os.add_dll_directory(dll_directory)
    print(f"✅ Added DLL directory: {dll_directory}")
else:
    print(f"❌ DLL directory not found: {dll_directory}")
    print("Please build the C library first with CMake")
    sys.exit(1)

# Now we can import the CFFI module
try:
    import _grass_datetime_cffi as cffi_module
    print("✅ Successfully imported CFFI module!")
except ImportError as e:
    print(f"❌ Failed to import CFFI module: {e}")
    sys.exit(1)

# Test basic functionality
def main():
    print("\n🌟 GRASS DateTime with os.add_dll_directory() Demo")
    print("=" * 55)
    
    ffi = cffi_module.ffi
    lib = cffi_module.lib
    
    # Test utility functions
    print("\n🛠️  Utility Functions:")
    print(f"📅 2024 is leap year: {lib.datetime_is_leap_year(2024, 1) != 0}")
    print(f"📅 Days in February 2024: {lib.datetime_days_in_month(2024, 2, 1)}")
    
    # Test DateTime structure
    print("\n🕐 DateTime Structure:")
    dt = ffi.new("DateTime *")
    
    # Set type and values
    lib.datetime_set_type(dt, lib.DATETIME_ABSOLUTE, lib.DATETIME_YEAR, lib.DATETIME_SECOND, 0)
    lib.datetime_set_year(dt, 2025)
    lib.datetime_set_month(dt, 8)
    lib.datetime_set_day(dt, 25)
    lib.datetime_set_hour(dt, 16)
    lib.datetime_set_minute(dt, 45)
    lib.datetime_set_second(dt, 30.0)
    
    # Format the datetime
    buffer = ffi.new("char[]", 256)
    if lib.datetime_format(dt, buffer) == 0:
        formatted = ffi.string(buffer).decode('utf-8')
        print(f"📝 Formatted datetime: {formatted}")
    
    print(f"🔍 Is absolute: {lib.datetime_is_absolute(dt) != 0}")
    print(f"🔍 Is positive: {lib.datetime_is_positive(dt) != 0}")
    
    print("\n✨ Demo completed successfully!")
    print("🎉 The DLL was loaded from PATH using os.add_dll_directory()!")

if __name__ == "__main__":
    main()
