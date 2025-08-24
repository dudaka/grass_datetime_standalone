#!/usr/bin/env python3
"""
Quick demo of the GRASS DateTime Python wrapper
"""

from grass_datetime import DateTime, days_in_month, is_leap_year

print('=== GRASS DateTime Python Wrapper Demo ===')

# Create datetime
dt = DateTime.absolute(2025, 8, 24, 14, 30, 45.5)
print(f'1. Created datetime: {dt}')

# Access components
print(f'2. Components: Year={dt.year}, Month={dt.month}, Day={dt.day}')

# Property modification
dt2 = DateTime.absolute(2025, 1, 1)
print(f'3. Initial date: {dt2}')
dt2.hour = 15
dt2.minute = 30
print(f'4. Modified time: {dt2}')

# Timezone operations
dt3 = DateTime.absolute(2025, 8, 24, 14, 30, 0, timezone_minutes=120)  # UTC+2
print(f'5. With timezone: {dt3}')

# Comparison
dt4 = DateTime.absolute(2025, 8, 24, 14, 30, 45.5)
print(f'6. Comparison: dt == dt4? {dt == dt4}')

# Utility functions
print(f'7. Is 2024 leap year? {is_leap_year(2024)}')
print(f'8. Days in Feb 2024: {days_in_month(2024, 2)}')

print('✅ Python wrapper working successfully!')
