#!/usr/bin/env python3
"""
Demo script for GRASS DateTime Python bindings
"""

import sys
import os

# Add the python directory to the path so we can import the module
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

def demo_basic_usage():
    """Demonstrate basic DateTime usage."""
    print("\n🕐 Basic DateTime Usage Demo")
    print("=" * 40)
    
    try:
        # Import the GRASS DateTime module
        from grass_datetime import DateTime, DateTimeError, ABSOLUTE, YEAR, SECOND, days_in_month, is_leap_year
        print("✅ Successfully imported GRASS DateTime module!")
        
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
        
    except ImportError as e:
        print(f"❌ Failed to import module: {e}")
        print("Make sure to build the C library first and run the build script.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def demo_utility_functions():
    """Demonstrate utility functions."""
    print("\n🛠️  Utility Functions Demo")
    print("=" * 40)
    
    try:
        from grass_datetime import days_in_month, is_leap_year
        
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

def main():
    """Main demo function."""
    print("🌟 GRASS DateTime Python Bindings Demo")
    print("=" * 50)
    
    # Run basic demo
    if demo_basic_usage():
        demo_utility_functions()
        print("\n✨ Demo completed successfully!")
    else:
        print("\n❌ Demo failed - check the build setup")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
