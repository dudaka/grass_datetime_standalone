# GRASS DateTime Python CFFI Bindings

Python bindings for the GRASS DateTime C library using CFFI (C Foreign Function Interface). This project provides both low-level CFFI access and a high-level Pythonic wrapper for GRASS GIS datetime functionality.

## Project Structure

This project follows a clean build architecture where:
- **Source files** stay in `python/` directory (this directory)
- **Generated files** (.dll, .pyd, .c) go to `build/` directory
- **CMake manages** the entire build process

```
datetime_standalone/
├── build/                          # All generated files
│   ├── grass_datetime.dll         # C shared library
│   ├── _grass_datetime_cffi.*.pyd  # Python CFFI extension
│   └── _grass_datetime_cffi.c      # Generated C wrapper
├── python/                         # Clean source directory  
│   ├── grass_datetime_build.py    # CFFI build script
│   ├── grass_datetime.py          # High-level Python wrapper
│   ├── test_direct.py             # Direct CFFI testing
│   └── README.md                  # This file
└── [C library source files]
```

## Quick Start

### 1. Build Everything with CMake

From the project root:

```bash
# Configure and build C library + Python extension
mkdir build
cd build
cmake .. -DBUILD_PYTHON_EXTENSION=ON
cmake --build . --config Release --target python_extension
```

### 2. Test from Build Directory

```bash
# From build/ directory, test direct CFFI
python -c "import sys; sys.path.insert(0, '.'); from _grass_datetime_cffi import lib; print('2024 is leap:', lib.datetime_is_leap_year(2024, 1) != 0)"

# Test high-level wrapper
python ../python/grass_datetime.py

# Test comprehensive functionality
python ../python/test_direct.py
```

### 3. Available CMake Targets

```bash
# Build Python CFFI extension
cmake --build . --config Release --target python_extension

# Run tests (from build directory)
cmake --build . --config Release --target test_python_direct
```

## Usage Examples

### Direct CFFI Interface (Low-Level)

Use this when you need direct access to C functions:

```python
import sys
sys.path.insert(0, '.')  # When running from build directory

from _grass_datetime_cffi import ffi, lib

# Test utility functions
leap = lib.datetime_is_leap_year(2024, 1) != 0
days = lib.datetime_days_in_month(2024, 2, 1)
print(f"2024 is leap year: {leap}")
print(f"Days in February 2024: {days}")

# Work with DateTime structures
dt = ffi.new("DateTime *")
lib.datetime_set_type(dt, lib.DATETIME_ABSOLUTE, lib.DATETIME_YEAR, lib.DATETIME_SECOND, 0)

# Set values
lib.datetime_set_year(dt, 2025)
lib.datetime_set_month(dt, 8)
lib.datetime_set_day(dt, 25)
lib.datetime_set_hour(dt, 14)
lib.datetime_set_minute(dt, 30)
lib.datetime_set_second(dt, 45.0)

# Format the datetime
buffer = ffi.new("char[]", 256)
if lib.datetime_format(dt, buffer) == 0:
    formatted = ffi.string(buffer).decode('utf-8')
    print(f"Formatted: {formatted}")  # "25 Aug 2025 14:30:45"
```

### High-Level Python Wrapper (Pythonic)

Use this for a more natural Python experience:

```python
import sys
import os
sys.path.insert(0, '.')  # For CFFI module (when from build dir)
sys.path.insert(0, os.path.join('..', 'python'))  # For wrapper

from grass_datetime import DateTime, is_leap_year, days_in_month, ABSOLUTE, YEAR, SECOND

# Utility functions
print(f"2024 is leap year: {is_leap_year(2024)}")
print(f"Days in February 2024: {days_in_month(2024, 2)}")

# Create DateTime object with Pythonic interface
dt = DateTime()
dt.set_type(ABSOLUTE, YEAR, SECOND, 0)

# Set values using properties
dt.year = 2025
dt.month = 8
dt.day = 25
dt.hour = 14
dt.minute = 30
dt.second = 45.5

# Easy access and formatting
print(f"Created: {dt}")                    # "25 Aug 2025 14:30:46"
print(f"Year: {dt.year}, Month: {dt.month}")  # "Year: 2025, Month: 8"
print(f"Time: {dt.hour}:{dt.minute:02d}:{dt.second:.1f}")

# Copy functionality
dt2 = dt.copy()
print(f"Copied: {dt2}")
```

## Available Functions

### Utility Functions
- `datetime_is_leap_year(year, ad)` - Check if year is leap year
- `datetime_days_in_month(year, month, ad)` - Get days in month  
- `datetime_days_in_year(year, ad)` - Get days in year

### DateTime Structure Operations
- `datetime_set_type(dt, mode, from, to, fracsec)` - Set datetime type
- `datetime_set_year/month/day/hour/minute/second(dt, value)` - Set values
- `datetime_get_year/month/day/hour/minute/second(dt, ptr)` - Get values
- `datetime_format(dt, buffer)` - Format as string
- `datetime_copy(src, dst)` - Copy datetime structure

### Constants
- `DATETIME_ABSOLUTE` (1) - Absolute datetime
- `DATETIME_RELATIVE` (2) - Relative datetime  
- `DATETIME_YEAR` (101) - Year precision
- `DATETIME_MONTH` (102) - Month precision
- `DATETIME_DAY` (103) - Day precision
- `DATETIME_HOUR` (104) - Hour precision
- `DATETIME_MINUTE` (105) - Minute precision
- `DATETIME_SECOND` (106) - Second precision

## Files Description

- **`grass_datetime_build.py`** - CFFI build script (matches sample project pattern)
- **`grass_datetime.py`** - High-level Pythonic wrapper with error handling
- **`test_direct.py`** - Direct CFFI testing script with comprehensive tests
- **`requirements.txt`** - Python dependencies (cffi)

## Build Process Details

### CFFI Build Script
The `grass_datetime_build.py` follows the sample project pattern exactly:
- Simplified `cdef()` with core functions only
- Proper `library_dirs` and `include_dirs` configuration
- Generates `.c` and `.pyd` files in build directory when run via CMake

### CMake Integration
- Custom `python_extension` target with correct `WORKING_DIRECTORY`
- Dependencies ensure C library is built first
- Cross-platform support (MSVC/GCC/Clang)

### DLL Loading
The Python wrapper automatically handles DLL path resolution:
- Works from build directory (primary method)
- Supports multiple directory layouts
- Uses `os.add_dll_directory()` on Windows

## Testing

### Manual Testing
```bash
# From build directory
python ../python/test_direct.py      # Comprehensive direct CFFI test
python ../python/grass_datetime.py   # High-level wrapper test
```

### CMake Testing
```bash
# From build directory
cmake --build . --config Release --target test_python_direct
```

## Troubleshooting

### Import Errors
- **Problem**: `ImportError: No module named '_grass_datetime_cffi'`
- **Solution**: Run from build directory with `sys.path.insert(0, '.')`

### DLL Not Found
- **Problem**: DLL loading fails
- **Solution**: Ensure you're running from build directory where .dll and .pyd files exist

### Build Errors
- **Problem**: CFFI compilation fails
- **Solution**: Ensure C library builds first, check MSVC compiler availability

### Encoding Errors  
- **Problem**: Unicode characters in Windows cmd.exe
- **Solution**: Scripts use plain text (no emoji) for Windows compatibility

## Requirements

- **Python 3.7+** with CFFI package
- **CMake 3.15+** for build system
- **MSVC** (Windows) or **GCC/Clang** (Linux/Mac) compiler
- **GRASS DateTime C library** (built automatically via CMake)

## Success Indicators

When everything is working correctly:
- ✅ Files `grass_datetime.dll` and `_grass_datetime_cffi.*.pyd` exist in `build/`
- ✅ `python -c "import sys; sys.path.insert(0, '.'); from _grass_datetime_cffi import lib; print(lib.datetime_is_leap_year(2024, 1))"`
- ✅ Both test scripts run without errors
- ✅ High-level wrapper provides Pythonic interface
