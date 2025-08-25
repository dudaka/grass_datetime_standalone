#!/usr/bin/env python3
"""
Simple test for GRASS DateTime Python bindings without relative imports
"""

import _grass_datetime_cffi as cffi_module

def test_basic_functionality():
    """Test basic CFFI functionality."""
    print("🌟 GRASS DateTime Python Bindings Test")
    print("=" * 50)
    
    # Access the FFI and library objects
    ffi = cffi_module.ffi
    lib = cffi_module.lib
    
    print("✅ Successfully imported CFFI module!")
    
    # Test utility functions first
    print("\n🛠️  Testing Utility Functions:")
    print("-" * 30)
    
    # Test leap year
    years = [2020, 2021, 2024, 2025]
    for year in years:
        leap = lib.datetime_is_leap_year(year, 1) != 0
        print(f"📅 {year} is {'a leap year' if leap else 'not a leap year'}")
    
    # Test days in month
    print(f"\n📅 Days in February 2024: {lib.datetime_days_in_month(2024, 2, 1)}")
    print(f"📅 Days in February 2025: {lib.datetime_days_in_month(2025, 2, 1)}")
    
    # Test DateTime structure
    print("\n🕐 Testing DateTime Structure:")
    print("-" * 30)
    
    # Create a DateTime structure
    dt = ffi.new("DateTime *")
    
    # Set type (ABSOLUTE, from YEAR to SECOND, 0 fracsec)
    result = lib.datetime_set_type(dt, lib.DATETIME_ABSOLUTE, lib.DATETIME_YEAR, lib.DATETIME_SECOND, 0)
    if result == 0:
        print("✅ Successfully set DateTime type")
    else:
        print(f"❌ Failed to set DateTime type: {result}")
        return
    
    # Set date and time values
    lib.datetime_set_year(dt, 2025)
    lib.datetime_set_month(dt, 8)
    lib.datetime_set_day(dt, 25)
    lib.datetime_set_hour(dt, 15)
    lib.datetime_set_minute(dt, 30)
    lib.datetime_set_second(dt, 45.5)
    
    print("✅ Set date and time values")
    
    # Get values back
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
    
    print(f"📅 Retrieved date: {year[0]}-{month[0]:02d}-{day[0]:02d}")
    print(f"🕐 Retrieved time: {hour[0]:02d}:{minute[0]:02d}:{second[0]:06.3f}")
    
    # Format the datetime
    buffer = ffi.new("char[]", 256)
    result = lib.datetime_format(dt, buffer)
    if result == 0:
        formatted = ffi.string(buffer).decode('utf-8')
        print(f"📝 Formatted: {formatted}")
    else:
        print(f"❌ Failed to format DateTime: {result}")
    
    # Test validation functions
    print(f"🔍 Is absolute: {lib.datetime_is_absolute(dt) != 0}")
    print(f"🔍 Is relative: {lib.datetime_is_relative(dt) != 0}")
    print(f"🔍 Is positive: {lib.datetime_is_positive(dt) != 0}")
    
    print("\n✨ All tests completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    test_basic_functionality()
