# GRASS DateTime Python Bindings

Python bindings for the GRASS DateTime C library using CFFI.

## Installation

### Prerequisites

1. **Build the C library first**:
   ```bash
   # From the project root
   mkdir build
   cd build
   cmake ..
   cmake --build . --config Release
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Build the Python Extension

1. **Navigate to the python directory**:
   ```bash
   cd python
   ```

2. **Build the CFFI extension**:
   ```bash
   python grass_datetime_build.py
   ```

3. **Copy the DLL** (Windows only):
   ```bash
   copy ..\build\Release\grass_datetime.dll .
   ```

## Usage

### Direct CFFI Usage

```python
import _grass_datetime_cffi as cffi_module

# Access FFI and library
ffi = cffi_module.ffi
lib = cffi_module.lib

# Test utility functions
leap = lib.datetime_is_leap_year(2024, 1) != 0
print(f"2024 is leap year: {leap}")

days = lib.datetime_days_in_month(2024, 2, 1)
print(f"Days in February 2024: {days}")

# Work with DateTime structures
dt = ffi.new("DateTime *")
lib.datetime_set_type(dt, lib.DATETIME_ABSOLUTE, lib.DATETIME_YEAR, lib.DATETIME_SECOND, 0)

# Set values
lib.datetime_set_year(dt, 2025)
lib.datetime_set_month(dt, 8)
lib.datetime_set_day(dt, 25)

# Format
buffer = ffi.new("char[]", 256)
if lib.datetime_format(dt, buffer) == 0:
    formatted = ffi.string(buffer).decode('utf-8')
    print(f"Formatted: {formatted}")
```

### High-Level Python Wrapper (Future)

The `grass_datetime.py` module provides a higher-level Python interface:

```python
from grass_datetime import DateTime, ABSOLUTE, YEAR, SECOND

# Create DateTime object
dt = DateTime(ABSOLUTE, YEAR, SECOND, 0)

# Set values using properties
dt.year = 2025
dt.month = 8
dt.day = 25
dt.hour = 15
dt.minute = 30
dt.second = 45.5

# Format and display
print(f"Formatted: {dt.format()}")
print(f"String representation: {str(dt)}")
```

## Testing

Run the direct test to verify functionality:

```bash
python direct_test.py
```

## Constants

Available constants from the C library:

- `DATETIME_ABSOLUTE` (1) - Absolute datetime
- `DATETIME_RELATIVE` (2) - Relative datetime
- `DATETIME_YEAR` (101) - Year precision
- `DATETIME_MONTH` (102) - Month precision
- `DATETIME_DAY` (103) - Day precision
- `DATETIME_HOUR` (104) - Hour precision
- `DATETIME_MINUTE` (105) - Minute precision
- `DATETIME_SECOND` (106) - Second precision

## Available Functions

### Utility Functions
- `datetime_is_leap_year(year, ad)` - Check if year is leap year
- `datetime_days_in_month(year, month, ad)` - Get days in month
- `datetime_days_in_year(year, ad)` - Get days in year

### DateTime Operations
- `datetime_set_type(dt, mode, from, to, fracsec)` - Set datetime type
- `datetime_set_year/month/day/hour/minute/second(dt, value)` - Set values
- `datetime_get_year/month/day/hour/minute/second(dt, ptr)` - Get values
- `datetime_format(dt, buffer)` - Format as string
- `datetime_scan(dt, string)` - Parse from string

### Validation
- `datetime_is_absolute(dt)` - Check if absolute
- `datetime_is_relative(dt)` - Check if relative
- `datetime_is_positive(dt)` - Check if positive
- `datetime_is_negative(dt)` - Check if negative

### Timezone
- `datetime_set_timezone(dt, minutes)` - Set timezone offset
- `datetime_get_timezone(dt, minutes_ptr)` - Get timezone offset
- `datetime_change_timezone(dt, minutes)` - Change timezone

## Files

- `grass_datetime_build.py` - CFFI build script
- `grass_datetime.py` - High-level Python wrapper
- `direct_test.py` - Direct CFFI testing
- `requirements.txt` - Python dependencies
- `setup.py` - Package setup script

## Troubleshooting

### DLL Not Found
- Ensure `grass_datetime.dll` is in the python directory
- Rebuild the C library if needed

### Import Errors
- Check that CFFI extension was built successfully
- Look for `_grass_datetime_cffi.cp*-win_amd64.pyd` file

### Build Errors
- Ensure MSVC is available in PATH
- Check that include and library paths are correct
- Verify the C library builds successfully first
