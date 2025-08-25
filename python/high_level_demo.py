#!/usr/bin/env python3
"""
Demo script showing how to use the high-level grass_datetime.py wrapper
"""

from grass_datetime import (
    DateTime, DateTimeError,
    days_in_month, is_leap_year, days_in_year,
    ABSOLUTE, RELATIVE,
    YEAR, MONTH, DAY, HOUR, MINUTE, SECOND
)

def demo_high_level_wrapper():
    """Demonstrate the high-level DateTime wrapper."""
    print("🌟 GRASS DateTime High-Level Python Wrapper Demo")
    print("=" * 55)
    
    try:
        # Create a new DateTime object
        print("\n📅 Creating DateTime object...")
        dt = DateTime(ABSOLUTE, YEAR, SECOND, 0)
        print("✅ Created DateTime object successfully!")
        
        # Set date and time using properties
        print("\n🕐 Setting date and time...")
        dt.year = 2025
        dt.month = 8
        dt.day = 25
        dt.hour = 16
        dt.minute = 45
        dt.second = 30.5
        
        print(f"   Year: {dt.year}")
        print(f"   Month: {dt.month}")
        print(f"   Day: {dt.day}")
        print(f"   Hour: {dt.hour}")
        print(f"   Minute: {dt.minute}")
        print(f"   Second: {dt.second}")
        
        # Alternative: set using methods
        print("\n🔧 Using setter methods...")
        dt2 = DateTime(ABSOLUTE, YEAR, SECOND, 0)
        dt2.set_year(2024)
        dt2.set_month(12)
        dt2.set_day(31)
        dt2.set_hour(23)
        dt2.set_minute(59)
        dt2.set_second(59.999)
        
        # Format the datetime
        print("\n📝 Formatting DateTimes...")
        formatted1 = dt.format()
        formatted2 = dt2.format()
        print(f"   DateTime 1: {formatted1}")
        print(f"   DateTime 2: {formatted2}")
        
        # String representations
        print(f"   String repr 1: {str(dt)}")
        print(f"   Object repr 1: {repr(dt)}")
        
        # Test properties and validation
        print("\n🔍 Properties and validation...")
        print(f"   Is absolute: {dt.is_absolute()}")
        print(f"   Is relative: {dt.is_relative()}")
        print(f"   Is positive: {dt.is_positive()}")
        print(f"   Is negative: {dt.is_negative()}")
        
        # Test timezone
        print("\n🌍 Timezone operations...")
        dt.set_timezone(120)  # UTC+2
        tz = dt.get_timezone()
        print(f"   Set timezone to UTC+{tz//60}:{abs(tz%60):02d}")
        
        # Test type information
        print("\n🔍 Type information...")
        mode, from_unit, to_unit, fracsec = dt.get_type()
        print(f"   Mode: {mode} ({'ABSOLUTE' if mode == ABSOLUTE else 'RELATIVE'})")
        print(f"   From unit: {from_unit}")
        print(f"   To unit: {to_unit}")
        print(f"   Fracsec: {fracsec}")
        
        # Test comparison
        print("\n⚖️  Comparison...")
        dt3 = DateTime(ABSOLUTE, YEAR, SECOND, 0)
        dt3.year = 2025
        dt3.month = 8
        dt3.day = 25
        dt3.hour = 16
        dt3.minute = 45
        dt3.second = 30.5
        
        print(f"   dt and dt3 are same: {dt.is_same(dt3)}")
        print(f"   dt and dt2 are same: {dt.is_same(dt2)}")
        
    except DateTimeError as e:
        print(f"❌ DateTime error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def demo_utility_functions():
    """Demonstrate utility functions."""
    print("\n\n🛠️  Utility Functions Demo")
    print("=" * 35)
    
    try:
        # Test leap years
        years = [2020, 2021, 2024, 2025, 2100, 2400]
        print("\n📅 Leap year tests:")
        for year in years:
            leap = is_leap_year(year)
            print(f"   {year}: {'leap year' if leap else 'not leap year'}")
        
        # Test days in month
        print("\n📅 Days in month tests:")
        months = [(2024, 2), (2025, 2), (2024, 4), (2024, 12)]
        for year, month in months:
            days = days_in_month(year, month)
            month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            print(f"   {month_names[month]} {year}: {days} days")
        
        # Test days in year
        print("\n📅 Days in year tests:")
        test_years = [2023, 2024, 2025]
        for year in test_years:
            days = days_in_year(year)
            print(f"   {year}: {days} days")
            
    except Exception as e:
        print(f"❌ Error in utility functions: {e}")

def demo_error_handling():
    """Demonstrate error handling."""
    print("\n\n⚠️  Error Handling Demo")
    print("=" * 30)
    
    try:
        dt = DateTime(ABSOLUTE, YEAR, SECOND, 0)
        
        # Try to set an invalid month
        print("\n🧪 Testing invalid month (13)...")
        dt.set_month(13)
        print("❌ This should have failed!")
        
    except DateTimeError as e:
        print(f"✅ Caught expected DateTime error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error type: {e}")
    
    try:
        # Try to set an invalid day
        print("\n🧪 Testing invalid day (32)...")
        dt = DateTime(ABSOLUTE, YEAR, SECOND, 0)
        dt.set_year(2025)
        dt.set_month(2)  # February
        dt.set_day(32)   # Invalid day for February
        print("❌ This should have failed!")
        
    except DateTimeError as e:
        print(f"✅ Caught expected DateTime error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error type: {e}")

def demo_constants():
    """Show available constants."""
    print("\n\n📋 Available Constants")
    print("=" * 25)
    
    print(f"DateTime modes:")
    print(f"   ABSOLUTE = {ABSOLUTE}")
    print(f"   RELATIVE = {RELATIVE}")
    
    print(f"\nTime units:")
    print(f"   YEAR = {YEAR}")
    print(f"   MONTH = {MONTH}")
    print(f"   DAY = {DAY}")
    print(f"   HOUR = {HOUR}")
    print(f"   MINUTE = {MINUTE}")
    print(f"   SECOND = {SECOND}")

def main():
    """Main demo function."""
    demo_high_level_wrapper()
    demo_utility_functions()
    demo_error_handling()
    demo_constants()
    
    print("\n" + "=" * 55)
    print("🎉 High-level wrapper demo completed successfully!")
    print("✨ You can now use grass_datetime.py in your projects!")
    print("=" * 55)

if __name__ == "__main__":
    main()
