#!/usr/bin/env python3
"""
Demo script for GRASS DateTime Python bindings
"""

import sys
import os

# Add the python directory to the path so we can import the module
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Import the GRASS DateTime module
try:
    from grass_datetime import DateTime, DateTimeError, ABSOLUTE, YEAR, SECOND, days_in_month, is_leap_year
    print("✅ Successfully imported GRASS DateTime module!")
except ImportError as e:
    print(f"❌ Failed to import module: {e}")
    print("Make sure to build the C library first and run the build script.")
    sys.exit(1)

def demo_basic_usage():
    """Demonstrate basic DateTime usage."""
    print("\n🕐 Basic DateTime Usage Demo")
    print("=" * 40)
    
    try:
        # Create a new DateTime object
        dt = DateTime(ABSOLUTE, YEAR, SECOND, 0)
        print("✅ Created DateTime object")
        
        # Set date and time
        dt.year = 2025
        dt.month = 8
        dt.day = 25
        dt.hour = 15
        dt.minute = 30
        dt.second = 45.5
        
        print(f"📅 Set date: {dt.year}-{dt.month:02d}-{dt.day:02d}")
        print(f"🕐 Set time: {dt.hour:02d}:{dt.minute:02d}:{dt.second:06.3f}")
        
        # Format the datetime
        formatted = dt.format()
        print(f"📝 Formatted: {formatted}")
        
        # Display properties
        print(f"🔍 Properties:")
        print(f"   - Is absolute: {dt.is_absolute()}")
        print(f"   - Is relative: {dt.is_relative()}")
        print(f"   - Is positive: {dt.is_positive()}")
        
        # String representation
        print(f"🔤 String representation: {str(dt)}")
        print(f"🔤 Object representation: {repr(dt)}")
        
    except DateTimeError as e:
        print(f"❌ DateTime error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def demo_utility_functions():
    """Demonstrate utility functions."""
    print("\n🛠️  Utility Functions Demo")
    print("=" * 40)
    
    try:
        # Test leap year
        years = [2020, 2021, 2024, 2025]
        for year in years:
            leap = is_leap_year(year)
            print(f"📅 {year} is {'a leap year' if leap else 'not a leap year'}")
        
        # Test days in month
        print(f"\n📅 Days in February 2024: {days_in_month(2024, 2)}")
        print(f"📅 Days in February 2025: {days_in_month(2025, 2)}")
        
    except Exception as e:
        print(f"❌ Error in utility functions: {e}")

def demo_error_handling():
    """Demonstrate error handling."""
    print("\n⚠️  Error Handling Demo")
    print("=" * 40)
    
    try:
        dt = DateTime()
        # Try to set an invalid date
        dt.set_month(13)  # Invalid month
        print("❌ This should have failed!")
    except DateTimeError as e:
        print(f"✅ Caught expected error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error type: {e}")

def demo_timezone_handling():
    """Demonstrate timezone handling."""
    print("\n🌍 Timezone Handling Demo")
    print("=" * 40)
    
    try:
        dt = DateTime(ABSOLUTE, YEAR, SECOND, 0)
        dt.year = 2025
        dt.month = 8
        dt.day = 25
        dt.hour = 12
        dt.minute = 0
        dt.second = 0
        
        print(f"🌍 Original time: {dt.format()}")
        
        # Set timezone to UTC+2 (120 minutes)
        dt.set_timezone(120)
        tz = dt.get_timezone()
        print(f"🌍 Timezone set to UTC+{tz//60}:{tz%60:02d}")
        
        # Set timezone to UTC-5 (-300 minutes)
        dt.set_timezone(-300)
        tz = dt.get_timezone()
        sign = '+' if tz >= 0 else '-'
        abs_tz = abs(tz)
        print(f"🌍 Timezone changed to UTC{sign}{abs_tz//60}:{abs_tz%60:02d}")
        
    except DateTimeError as e:
        print(f"❌ Timezone error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main demo function."""
    print("🌟 GRASS DateTime Python Bindings Demo")
    print("=" * 50)
    
    # Run all demos
    demo_basic_usage()
    demo_utility_functions()
    demo_error_handling()
    demo_timezone_handling()
    
    print("\n✨ Demo completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
