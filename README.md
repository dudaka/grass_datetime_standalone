# GRASS DateTime Library

A standalone C library for date and time operations extracted from GRASS GIS, with Python bindings.

## Features

- Date and time parsing and formatting
- Time zone handling  
- Date arithmetic and comparisons
- Cross-platform support (Windows, Linux, macOS)
- **Python bindings** for easy integration

## Quick Start

### C Library

1. **Build**:

   ```bash
   mkdir build && cd build
   cmake ..
   cmake --build . --config Release
   ```

2. **Test**:

   ```bash
   ctest -C Release
   ```

### Python Bindings

1. **Build the C library first** (see above)

2. **Build Python extension**:

   ```bash
   cd python
   python grass_datetime_build.py
   ```

3. **Use it**:

   ```python
   from grass_datetime import DateTime, ABSOLUTE, YEAR, SECOND
   
   # Create datetime
   dt = DateTime(ABSOLUTE, YEAR, SECOND, 0)
   dt.year = 2025
   dt.month = 8
   dt.day = 25
   
   print(dt)  # Output: 25 Aug 2025 00:00:00
   ```

## Examples

### C Usage

```c
#include <grass/datetime.h>

DateTime dt;
datetime_set_type(&dt, DATETIME_ABSOLUTE, DATETIME_YEAR, DATETIME_SECOND, 0);
datetime_set_year(&dt, 2025);
datetime_set_month(&dt, 8);
datetime_set_day(&dt, 25);

char buffer[100];
datetime_format(&dt, buffer);
printf("Date: %s\n", buffer);
```

### Python Usage

```python
from grass_datetime import DateTime, is_leap_year, days_in_month

# Create and use datetime
dt = DateTime()
dt.year = 2025
dt.month = 2
dt.day = 14

print(f"Date: {dt}")
print(f"Is 2024 leap year: {is_leap_year(2024)}")
print(f"Days in Feb 2024: {days_in_month(2024, 2)}")
```

## File Structure

```text
├── include/grass/          # Header files
├── lib/datetime/          # C source files
├── python/               # Python bindings
├── test_datetime.c       # C test file
└── CMakeLists.txt       # Build configuration
```

## Documentation

- **C API**: See header files in `include/grass/`
- **Python API**: Run `python python/high_level_demo.py` for examples
- **Build Details**: See `python/README.md` for Python-specific info
