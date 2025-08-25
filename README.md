# GRASS DateTime Library - Standalone C Library with Python CFFI Bindings

A comprehensive standalone implementation of the GRASS GIS DateTime library with modern Python bindings via CFFI. This project provides both a high-performance C library and a Pythonic interface for date/time operations.

## ✅ Project Status: COMPLETE

- ✅ **C Library**: Full GRASS DateTime functionality with MSVC/GCC support
- ✅ **Python CFFI Bindings**: Both low-level CFFI and high-level wrapper
- ✅ **CMake Build System**: Modern cross-platform build configuration
- ✅ **Clean Architecture**: Generated files in build/, source files stay clean
- ✅ **Comprehensive Testing**: Multiple test approaches validate all functionality

## Features

- **Date/Time Operations**: Parsing, formatting, validation, and arithmetic
- **Time Zone Support**: UTC offset handling and conversion
- **Cross-Platform**: Windows (MSVC), Linux/Mac (GCC/Clang) support
- **Python Integration**: CFFI-based bindings with Pythonic wrapper
- **High Performance**: Direct C library access with minimal overhead
- **Clean Build**: Source and generated files properly separated

## Quick Start

### 🔧 Build Everything (C Library + Python Bindings)

```bash
# Clone or navigate to project
cd datetime_standalone

# Configure and build everything
mkdir build && cd build
cmake .. -DBUILD_PYTHON_EXTENSION=ON
cmake --build . --config Release --target python_extension

# Verify build success
dir *.dll *.pyd  # Should show grass_datetime.dll and _grass_datetime_cffi.*.pyd
```

### 🧪 Test Everything Works

```bash
# Quick CFFI test (from build directory)
python -c "import sys; sys.path.insert(0, '.'); from _grass_datetime_cffi import lib; print('2024 is leap:', lib.datetime_is_leap_year(2024, 1) != 0)"

# Comprehensive tests
python ../python/test_direct.py      # Direct CFFI interface
python ../python/grass_datetime.py   # High-level Python wrapper
```

## Usage Examples

### 🐍 Python High-Level Interface (Recommended)

```python
import sys, os
sys.path.insert(0, '.')  # For CFFI module (when from build dir)
sys.path.insert(0, os.path.join('..', 'python'))  # For wrapper

from grass_datetime import DateTime, is_leap_year, days_in_month, ABSOLUTE, YEAR, SECOND

# Utility functions
print(f"2024 is leap year: {is_leap_year(2024)}")        # True
print(f"Days in February 2024: {days_in_month(2024, 2)}") # 29

# DateTime object with Pythonic interface
dt = DateTime()
dt.set_type(ABSOLUTE, YEAR, SECOND, 0)
dt.year = 2025
dt.month = 8
dt.day = 25
dt.hour = 14
dt.minute = 30
dt.second = 45.5

print(f"Formatted: {dt}")                               # "25 Aug 2025 14:30:46"
print(f"Components: {dt.year}-{dt.month:02d}-{dt.day:02d}")  # "2025-08-25"

# Copy and manipulate
dt2 = dt.copy()
dt2.month = 12
print(f"Modified copy: {dt2}")                          # "25 Dec 2025 14:30:46"
```

### ⚡ Direct CFFI Interface (Low-Level)

```python
import sys
sys.path.insert(0, '.')  # When running from build directory

from _grass_datetime_cffi import ffi, lib

# Utility functions
leap = lib.datetime_is_leap_year(2024, 1) != 0
days = lib.datetime_days_in_month(2024, 2, 1)

# DateTime structure manipulation
dt = ffi.new("DateTime *")
lib.datetime_set_type(dt, lib.DATETIME_ABSOLUTE, lib.DATETIME_YEAR, lib.DATETIME_SECOND, 0)
lib.datetime_set_year(dt, 2025)
lib.datetime_set_month(dt, 8)
lib.datetime_set_day(dt, 25)

# Format output
buffer = ffi.new("char[]", 256)
lib.datetime_format(dt, buffer)
formatted = ffi.string(buffer).decode('utf-8')
print(f"Formatted: {formatted}")  # "25 Aug 2025 00:00:00"
```

### 🔧 C Library Usage

```c
#include <grass/datetime.h>

DateTime dt;
datetime_set_type(&dt, DATETIME_ABSOLUTE, DATETIME_YEAR, DATETIME_SECOND, 0);
datetime_set_year(&dt, 2025);
datetime_set_month(&dt, 8);
datetime_set_day(&dt, 25);

char buffer[100];
datetime_format(&dt, buffer);
printf("Date: %s\n", buffer);  // "25 Aug 2025 00:00:00"

// Utility functions
int leap = datetime_is_leap_year(2024, 1);  // 1 (true)
int days = datetime_days_in_month(2024, 2, 1);  // 29
```

## Project Architecture

### Clean Build Separation
```
datetime_standalone/
├── build/                          # 🏗️  All generated files
│   ├── grass_datetime.dll         # C shared library (31,744 bytes)
│   ├── _grass_datetime_cffi.*.pyd  # Python extension (24,576 bytes)
│   └── _grass_datetime_cffi.c      # Generated CFFI wrapper
├── python/                         # 📁 Clean source directory
│   ├── grass_datetime_build.py    # CFFI build script
│   ├── grass_datetime.py          # High-level Python wrapper
│   ├── test_direct.py             # Comprehensive testing
│   └── README.md                  # Python-specific documentation
├── include/grass/                  # 📋 C headers
│   ├── datetime.h                 # Main DateTime API
│   └── defs/datetime.h            # Function declarations
├── lib/datetime/                   # 🔧 C implementation
│   ├── *.c                        # DateTime functions
│   └── CMakeLists.txt             # Build configuration
└── CMakeLists.txt                 # 🏭 Main build system
```

### Available CMake Targets

```bash
# Build C library only
cmake --build . --config Release --target grass_datetime

# Build Python CFFI extension 
cmake --build . --config Release --target python_extension

# Run tests
cmake --build . --config Release --target test_python_direct
ctest -C Release  # C library tests
```

## Available Functions

### DateTime Operations
- `datetime_set_type()` - Configure datetime type and precision
- `datetime_set_*()` - Set year, month, day, hour, minute, second
- `datetime_get_*()` - Retrieve individual components
- `datetime_format()` - Format as human-readable string
- `datetime_copy()` - Copy datetime structures

### Utility Functions  
- `datetime_is_leap_year()` - Check leap year status
- `datetime_days_in_month()` - Days in specific month/year
- `datetime_days_in_year()` - Days in specific year

### Python High-Level Features
- **Property Access**: `dt.year = 2025`, `dt.month = 8`
- **Object Copying**: `dt2 = dt.copy()`
- **String Representation**: `str(dt)`, `repr(dt)`
- **Error Handling**: Pythonic exceptions
- **Type Safety**: Automatic validation

## Requirements

- **C Compiler**: MSVC (Windows) or GCC/Clang (Linux/Mac)
- **CMake**: 3.15 or higher
- **Python**: 3.7+ with CFFI package (`pip install cffi`)

## Testing & Validation

### Test Suite Results
- ✅ **Direct CFFI**: Module imports, basic functions, DateTime structures
- ✅ **High-Level Wrapper**: Object interface, properties, copy functionality  
- ✅ **Build System**: CMake targets, cross-platform compilation
- ✅ **File Architecture**: Clean separation of source vs generated files

### Success Indicators
- Files `grass_datetime.dll` and `_grass_datetime_cffi.*.pyd` in `build/`
- No generated files in `python/` source directory
- All test scripts run without errors
- Both CFFI and wrapper interfaces functional

## Documentation

- **📖 Python API**: See `python/README.md` for detailed Python usage
- **🔧 C API**: Header files in `include/grass/` with full function documentation
- **🏗️ Build System**: CMake configuration supports Windows/Linux/Mac
- **🧪 Testing**: Multiple test scripts demonstrate functionality

## Troubleshooting

**Import Errors**: Ensure you're running from `build/` directory with proper `sys.path`  
**DLL Not Found**: Check that both `.dll` and `.pyd` files exist in `build/` directory  
**Build Errors**: Verify CMake 3.15+, MSVC/GCC available, and C library builds successfully

---

**🎉 This project provides a complete, working implementation of GRASS DateTime functionality with modern Python bindings. All components are tested and ready for use!**
