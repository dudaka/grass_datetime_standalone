#!/usr/bin/env python3
"""
Test script for GRASS DateTime Python wrapper.

This script demonstrates the usage of the Python wrapper for the GRASS DateTime library.
"""

import sys
import os

# Add the current directory to Python path so we can import grass_datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from grass_datetime import DateTime, DateTimeError, days_in_month, is_leap_year, days_in_year
    print("✓ Successfully imported GRASS DateTime Python wrapper")
except ImportError as e:
    print(f"✗ Failed to import wrapper: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error loading GRASS DateTime library: {e}")
    print("Make sure the library is built and available in build/lib/datetime/Release/")
    sys.exit(1)

def test_basic_functionality():
    """Test basic DateTime functionality."""
    print("\n=== Testing Basic Functionality ===")
    
    try:
        # Create absolute datetime
        dt = DateTime.absolute(2025, 8, 24, 14, 30, 45.5)
        print(f"✓ Created absolute datetime: {dt}")
        
        # Test property access
        print(f"✓ Year: {dt.year}, Month: {dt.month}, Day: {dt.day}")
        print(f"✓ Hour: {dt.hour}, Minute: {dt.minute}, Second: {dt.second}")
        print(f"✓ Is absolute: {dt.is_absolute()}, Is relative: {dt.is_relative()}")
        
        # Create relative datetime (interval)
        interval = DateTime.relative(hours=2, minutes=30, seconds=15.25)
        print(f"✓ Created relative datetime: {interval}")
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False
    
    return True

def test_property_modification():
    """Test modifying DateTime properties."""
    print("\n=== Testing Property Modification ===")
    
    try:
        dt = DateTime.absolute(2025, 1, 1)
        print(f"✓ Initial datetime: {dt}")
        
        # Modify properties
        dt.month = 12
        dt.day = 31
        dt.hour = 23
        dt.minute = 59
        dt.second = 59.999
        
        print(f"✓ Modified datetime: {dt}")
        print(f"✓ Final values - Year: {dt.year}, Month: {dt.month}, Day: {dt.day}")
        
    except Exception as e:
        print(f"✗ Property modification test failed: {e}")
        return False
    
    return True

def test_datetime_operations():
    """Test DateTime arithmetic operations."""
    print("\n=== Testing DateTime Operations ===")
    
    try:
        # Create two datetimes
        dt1 = DateTime.absolute(2025, 8, 24, 12, 0, 0)
        dt2 = DateTime.absolute(2025, 8, 24, 14, 30, 0)
        print(f"✓ DateTime 1: {dt1}")
        print(f"✓ DateTime 2: {dt2}")
        
        # Test equality
        dt3 = DateTime.absolute(2025, 8, 24, 12, 0, 0)
        print(f"✓ dt1 == dt3: {dt1 == dt3}")
        print(f"✓ dt1 == dt2: {dt1 == dt2}")
        
        # Test difference
        diff = dt2.difference(dt1)
        print(f"✓ Difference (dt2 - dt1): {diff}")
        
        # Test addition
        interval = DateTime.relative(hours=1, minutes=15)
        result = dt1.add(interval)
        print(f"✓ dt1 + interval: {result}")
        
    except Exception as e:
        print(f"✗ DateTime operations test failed: {e}")
        return False
    
    return True

def test_timezone_operations():
    """Test timezone-related functionality."""
    print("\n=== Testing Timezone Operations ===")
    
    try:
        # Create datetime with timezone
        dt = DateTime.absolute(2025, 8, 24, 14, 30, 0, timezone_minutes=120)  # UTC+2
        print(f"✓ DateTime with timezone: {dt}")
        print(f"✓ Timezone offset: {dt.timezone_minutes} minutes")
        
        # Convert to different timezone
        dt.change_timezone(0)  # UTC
        print(f"✓ Converted to UTC: {dt}")
        
        # Convert to UTC using dedicated method
        dt.timezone_minutes = 300  # UTC+5
        print(f"✓ Set to UTC+5: {dt}")
        dt.to_utc()
        print(f"✓ Converted to UTC: {dt}")
        
    except Exception as e:
        print(f"✗ Timezone operations test failed: {e}")
        return False
    
    return True

def test_utility_functions():
    """Test utility functions."""
    print("\n=== Testing Utility Functions ===")
    
    try:
        year = 2025
        print(f"✓ Is {year} a leap year? {is_leap_year(year)}")
        print(f"✓ Days in {year}: {days_in_year(year)}")
        
        for month in [1, 2, 4, 12]:
            days = days_in_month(year, month)
            print(f"✓ Days in {year}-{month:02d}: {days}")
        
        # Test leap year
        leap_year = 2024
        print(f"✓ Is {leap_year} a leap year? {is_leap_year(leap_year)}")
        print(f"✓ Days in February {leap_year}: {days_in_month(leap_year, 2)}")
        
    except Exception as e:
        print(f"✗ Utility functions test failed: {e}")
        return False
    
    return True

def test_error_handling():
    """Test error handling."""
    print("\n=== Testing Error Handling ===")
    
    try:
        # Test invalid date
        try:
            dt = DateTime.absolute(2025, 13, 1)  # Invalid month
            print("✗ Should have failed for invalid month")
            return False
        except DateTimeError:
            print("✓ Correctly caught invalid month error")
        
        # Test invalid day
        try:
            dt = DateTime.absolute(2025, 2, 30)  # Invalid day for February
            print("✗ Should have failed for invalid day")
            return False
        except DateTimeError:
            print("✓ Correctly caught invalid day error")
        
        # Test invalid time
        try:
            dt = DateTime.absolute(2025, 8, 24, 25, 0, 0)  # Invalid hour
            print("✗ Should have failed for invalid hour")
            return False
        except DateTimeError:
            print("✓ Correctly caught invalid hour error")
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False
    
    return True

def test_string_representations():
    """Test string formatting and representations."""
    print("\n=== Testing String Representations ===")
    
    try:
        # Test absolute datetime formatting
        dt = DateTime.absolute(2025, 8, 24, 14, 30, 45)
        print(f"✓ Absolute datetime str(): {str(dt)}")
        print(f"✓ Absolute datetime repr(): {repr(dt)}")
        
        # Test relative datetime formatting
        interval = DateTime.relative(days=2, hours=3, minutes=45)
        print(f"✓ Relative datetime str(): {str(interval)}")
        print(f"✓ Relative datetime repr(): {repr(interval)}")
        
        # Test with different precisions
        dt_precise = DateTime.absolute(2025, 8, 24, 14, 30, 45.123456)
        print(f"✓ Precise datetime: {dt_precise}")
        
    except Exception as e:
        print(f"✗ String representations test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("GRASS DateTime Python Wrapper Test Suite")
    print("=" * 50)
    
    tests = [
        test_basic_functionality,
        test_property_modification,
        test_datetime_operations,
        test_timezone_operations,
        test_utility_functions,
        test_error_handling,
        test_string_representations,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Python wrapper is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
