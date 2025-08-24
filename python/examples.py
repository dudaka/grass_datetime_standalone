#!/usr/bin/env python3
"""
GRASS DateTime Python Wrapper - Usage Examples

This file demonstrates common usage patterns of the Python wrapper.
"""

from grass_datetime import DateTime, DateTimeError, days_in_month, is_leap_year, days_in_year

def main():
    print("GRASS DateTime Python Wrapper - Usage Examples")
    print("=" * 50)
    
    # Example 1: Create absolute datetimes
    print("\n1. Creating Absolute DateTimes")
    print("-" * 30)
    
    # Current moment
    now = DateTime.absolute(2025, 8, 24, 14, 30, 45.5)
    print(f"Current time: {now}")
    
    # Just date
    date_only = DateTime.absolute(2025, 12, 25)
    print(f"Christmas 2025: {date_only}")
    
    # With timezone (UTC+5)
    with_tz = DateTime.absolute(2025, 8, 24, 14, 30, 0, timezone_minutes=300)
    print(f"Time with timezone: {with_tz}")
    
    # Example 2: Create relative datetimes (intervals)
    print("\n2. Creating Relative DateTimes (Intervals)")
    print("-" * 30)
    
    # Various intervals
    two_hours = DateTime.relative(hours=2)
    print(f"Two hours: {two_hours}")
    
    week = DateTime.relative(days=7)
    print(f"One week: {week}")
    
    complex_interval = DateTime.relative(days=3, hours=2, minutes=30, seconds=15.5)
    print(f"Complex interval: {complex_interval}")
    
    # Example 3: DateTime arithmetic
    print("\n3. DateTime Arithmetic")
    print("-" * 30)
    
    start_time = DateTime.absolute(2025, 8, 24, 9, 0, 0)
    print(f"Meeting start: {start_time}")
    
    duration = DateTime.relative(hours=1, minutes=30)
    print(f"Meeting duration: {duration}")
    
    end_time = start_time.add(duration)
    print(f"Meeting end: {end_time}")
    
    # Calculate difference
    lunch_time = DateTime.absolute(2025, 8, 24, 12, 30, 0)
    break_duration = lunch_time.difference(end_time)
    print(f"Break until lunch: {break_duration}")
    
    # Example 4: Property access and modification
    print("\n4. Property Access and Modification")
    print("-" * 30)
    
    dt = DateTime.absolute(2025, 1, 1, 0, 0, 0)
    print(f"New Year: {dt}")
    print(f"Individual components: {dt.year}-{dt.month:02d}-{dt.day:02d} {dt.hour:02d}:{dt.minute:02d}:{dt.second:06.3f}")
    
    # Modify to New Year's Eve
    dt.month = 12
    dt.day = 31
    dt.hour = 23
    dt.minute = 59
    dt.second = 59.999
    print(f"New Year's Eve: {dt}")
    
    # Example 5: Timezone operations
    print("\n5. Timezone Operations")
    print("-" * 30)
    
    local_time = DateTime.absolute(2025, 8, 24, 14, 30, 0, timezone_minutes=120)  # UTC+2
    print(f"Local time (UTC+2): {local_time}")
    print(f"Timezone offset: {local_time.timezone_minutes} minutes")
    
    # Convert to UTC
    local_time.to_utc()
    print(f"Converted to UTC: {local_time}")
    
    # Change to different timezone
    local_time.change_timezone(-300)  # UTC-5 (EST)
    print(f"Converted to EST (UTC-5): {local_time}")
    
    # Example 6: Utility functions
    print("\n6. Utility Functions")
    print("-" * 30)
    
    year = 2024
    print(f"Is {year} a leap year? {is_leap_year(year)}")
    print(f"Days in {year}: {days_in_year(year)}")
    print(f"Days in February {year}: {days_in_month(year, 2)}")
    
    # Example 7: Comparison operations
    print("\n7. Comparison Operations")
    print("-" * 30)
    
    dt1 = DateTime.absolute(2025, 8, 24, 12, 0, 0)
    dt2 = DateTime.absolute(2025, 8, 24, 12, 0, 0)
    dt3 = DateTime.absolute(2025, 8, 24, 13, 0, 0)
    
    print(f"dt1: {dt1}")
    print(f"dt2: {dt2}")
    print(f"dt3: {dt3}")
    print(f"dt1 == dt2: {dt1 == dt2}")
    print(f"dt1 == dt3: {dt1 == dt3}")
    
    # Example 8: Error handling
    print("\n8. Error Handling")
    print("-" * 30)
    
    try:
        invalid_date = DateTime.absolute(2025, 2, 30)  # February doesn't have 30 days
        print(f"This shouldn't print: {invalid_date}")
    except DateTimeError as e:
        print(f"Caught expected error: {e}")
    
    try:
        invalid_time = DateTime.absolute(2025, 8, 24, 25, 0, 0)  # 25 is invalid hour
        print(f"This shouldn't print: {invalid_time}")
    except DateTimeError as e:
        print(f"Caught expected error: {e}")
    
    # Example 9: Working with different date formats
    print("\n9. Different Date Precision")
    print("-" * 30)
    
    year_only = DateTime.absolute(2025)
    print(f"Year only: {year_only}")
    
    year_month = DateTime.absolute(2025, 8)
    print(f"Year and month: {year_month}")
    
    full_date = DateTime.absolute(2025, 8, 24)
    print(f"Full date: {full_date}")
    
    with_time = DateTime.absolute(2025, 8, 24, 14, 30)
    print(f"Date with time: {with_time}")
    
    precise = DateTime.absolute(2025, 8, 24, 14, 30, 45.123456)
    print(f"High precision: {precise}")
    
    print("\n" + "=" * 50)
    print("All examples completed successfully! 🎉")

if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"Error: Could not import grass_datetime module: {e}")
        print("Make sure:")
        print("1. CFFI is installed: pip install cffi")
        print("2. The GRASS DateTime library is built in build/lib/datetime/Release/")
        print("3. The grass_datetime.py file is in the current directory")
    except Exception as e:
        print(f"Error running examples: {e}")
