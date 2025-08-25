#!/usr/bin/env python3
"""
Simple usage examples for grass_datetime.py
"""

from grass_datetime import DateTime, ABSOLUTE, YEAR, DAY, HOUR, MINUTE, SECOND, is_leap_year, days_in_month

def basic_usage():
    """Basic usage examples."""
    print("🌟 Basic Usage Examples")
    print("=" * 30)
    
    # Example 1: Create and set a datetime
    print("\n📅 Example 1: Create and set datetime")
    dt = DateTime(ABSOLUTE, YEAR, SECOND, 0)
    dt.year = 2025
    dt.month = 8
    dt.day = 25
    dt.hour = 14
    dt.minute = 30
    dt.second = 45
    
    print(f"Created: {dt}")
    
    # Example 2: Get individual components
    print("\n📊 Example 2: Get components")
    print(f"Year: {dt.year}")
    print(f"Month: {dt.month}")  
    print(f"Day: {dt.day}")
    print(f"Time: {dt.hour}:{dt.minute:02d}:{dt.second:04.1f}")
    
    # Example 3: Utility functions
    print("\n🛠️  Example 3: Utility functions")
    print(f"Is 2024 a leap year? {is_leap_year(2024)}")
    print(f"Days in February 2024: {days_in_month(2024, 2)}")
    
    # Example 4: Current time (sort of)
    print("\n🕐 Example 4: Set current-like time")
    now = DateTime(ABSOLUTE, YEAR, SECOND, 0)
    now.year = 2025
    now.month = 8
    now.day = 25
    now.hour = 17
    now.minute = 0
    now.second = 0
    print(f"Current-like time: {now}")
    
    # Example 5: Parse vs Create
    print("\n🔄 Example 5: Different precisions")
    # Date only (year to day)
    date_only = DateTime(ABSOLUTE, YEAR, DAY, 0)  # YEAR to DAY
    date_only.year = 2025
    date_only.month = 12
    date_only.day = 31
    print(f"Date only: {date_only}")
    
    # Time with minutes precision
    time_min = DateTime(ABSOLUTE, YEAR, MINUTE, 0)  # YEAR to MINUTE
    time_min.year = 2025
    time_min.month = 8
    time_min.day = 25
    time_min.hour = 15
    time_min.minute = 30
    print(f"Time (minutes): {time_min}")

if __name__ == "__main__":
    basic_usage()
