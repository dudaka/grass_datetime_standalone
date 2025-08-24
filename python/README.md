# GRASS DateTime Python Wrapper

A comprehensive Python wrapper for the GRASS DateTime library using CFFI, providing easy-to-use Python interfaces for date/time operations.

## Installation

### Prerequisites
- Python 3.7+
- CFFI package: `pip install cffi`
- Built GRASS DateTime library (see main README.md)

### Setup
1. Build the GRASS DateTime library:
   ```bash
   build.bat  # Windows
   # or
   ./build.sh  # Linux/Unix
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. The wrapper will automatically find the library in `build/lib/datetime/Release/`

## Usage

### Basic Examples

```python
from grass_datetime import DateTime, DateTimeError

# Create absolute datetime (specific date/time)
dt = DateTime.absolute(2025, 8, 24, 14, 30, 45.5)
print(dt)  # "24 Aug 2025 14:30:46"

# Create with just date
date_only = DateTime.absolute(2025, 12, 25)
print(date_only)  # "25 Dec 2025"

# With timezone (UTC+2 = 120 minutes)
with_tz = DateTime.absolute(2025, 8, 24, 14, 30, 0, timezone_minutes=120)
print(with_tz)  # "24 Aug 2025 14:30:00 +0200"
```

### Property Access and Modification

```python
dt = DateTime.absolute(2025, 1, 1)
print(f"Year: {dt.year}, Month: {dt.month}, Day: {dt.day}")

# Modify properties (automatically expands precision)
dt.hour = 23
dt.minute = 59
dt.second = 59.999
print(dt)  # Updated with time components
```

### DateTime Operations

```python
# Create two datetimes
dt1 = DateTime.absolute(2025, 8, 24, 12, 0, 0)
dt2 = DateTime.absolute(2025, 8, 24, 14, 30, 0)

# Calculate difference
diff = dt2.difference(dt1)
print(diff)  # "0 days 2 hours 30 minutes 0 seconds"

# Comparison
print(dt1 == dt2)  # False
```

### Timezone Operations

```python
# Create datetime with timezone
local_time = DateTime.absolute(2025, 8, 24, 14, 30, 0, timezone_minutes=120)
print(f"Local time: {local_time}")

# Convert to UTC
local_time.to_utc()
print(f"UTC time: {local_time}")

# Change to different timezone
local_time.change_timezone(-300)  # EST (UTC-5)
print(f"EST time: {local_time}")
```

### Utility Functions

```python
from grass_datetime import days_in_month, is_leap_year, days_in_year

print(f"Is 2024 a leap year? {is_leap_year(2024)}")  # True
print(f"Days in February 2024: {days_in_month(2024, 2)}")  # 29
print(f"Days in 2024: {days_in_year(2024)}")  # 366
```

### Error Handling

```python
try:
    invalid_date = DateTime.absolute(2025, 2, 30)  # Feb doesn't have 30 days
except DateTimeError as e:
    print(f"Error: {e}")
```

## API Reference

### DateTime Class

#### Class Methods
- `DateTime.absolute(year, month=None, day=None, hour=None, minute=None, second=None, timezone_minutes=None)` - Create absolute datetime
- `DateTime.relative(*args)` - Create relative datetime (partial support)
- `DateTime.parse(date_string)` - Parse datetime from string

#### Properties
- `year`, `month`, `day`, `hour`, `minute`, `second` - Date/time components
- `timezone_minutes` - Timezone offset in minutes from UTC

#### Methods
- `format()` - Format as string
- `is_absolute()`, `is_relative()` - Check datetime type
- `is_same(other)` - Compare with another datetime
- `difference(other)` - Calculate difference
- `add(interval)` - Add time interval (limited support)
- `to_utc()` - Convert to UTC
- `change_timezone(minutes)` - Change timezone

### Utility Functions
- `days_in_month(year, month)` - Days in given month/year
- `is_leap_year(year)` - Check if year is leap year
- `days_in_year(year)` - Days in given year

### Constants
- `DATETIME_ABSOLUTE`, `DATETIME_RELATIVE` - DateTime modes
- `DATETIME_YEAR`, `DATETIME_MONTH`, `DATETIME_DAY`, `DATETIME_HOUR`, `DATETIME_MINUTE`, `DATETIME_SECOND` - Precision constants

## Testing

Run the test suite:
```bash
python test_python_wrapper.py
```

Run examples:
```bash
python examples.py
```

## Current Status

✅ **Working Features:**
- Absolute datetime creation and manipulation
- Property access and modification with automatic precision expansion
- DateTime comparison and difference calculations
- Timezone operations (set, convert, UTC conversion)
- Utility functions (leap year, days in month/year)
- Comprehensive error handling
- String formatting and representation

⚠️ **Partial Support:**
- Relative datetime creation (some limitations with GRASS library constraints)
- DateTime arithmetic operations (basic support)

🔧 **Technical Details:**
- Uses CFFI for seamless C library integration
- Automatic library loading from build directory
- Proper error handling with descriptive messages
- Pythonic API design with properties and operators

## Troubleshooting

### Library Loading Issues
If you get library loading errors:
1. Ensure the library is built: run `build.bat` or `./build.sh`
2. Check that `grass_datetime.dll` (Windows) or equivalent shared library exists
3. On Windows, the DLL might need to be in the current directory

### Function Not Found Errors
If you get "function not found" errors, the library might not be exporting symbols properly. Rebuild with:
```bash
cd build
cmake --build . --config Release
```

## License

This wrapper maintains the same GPL v2+ license as the original GRASS DateTime library.
