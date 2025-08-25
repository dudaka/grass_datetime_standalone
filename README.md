# GRASS DateTime Library

A standalone C library for date and time operations extracted from GRASS GIS.

## Features

- Date and time parsing and formatting
- Time zone handling
- Date arithmetic and comparisons
- Cross-platform support (Windows, Linux, macOS)

## Building

### Prerequisites

- CMake 3.10 or higher
- A C compiler (MSVC on Windows, GCC/Clang on Unix-like systems)

### Build Steps

1. Create a build directory:
   ```bash
   mkdir build
   cd build
   ```

2. Configure the project:
   ```bash
   cmake ..
   ```

3. Build the library:
   ```bash
   cmake --build . --config Release
   ```

4. Run tests:
   ```bash
   ctest -C Release
   ```

### Manual Build (Windows with MSVC)

If you prefer to build manually on Windows:

```cmd
cl /LD /Iinclude /DGRASS_DATETIME_DLL_EXPORT /Fe:grass_datetime.dll lib\datetime\*.c
cl /Iinclude /Fe:test_datetime.exe test_datetime.c grass_datetime.lib
test_datetime.exe
```

## Usage

Include the header files and link against the shared library:

```c
#include <grass/datetime.h>

int main() {
    DateTime dt;
    
    // Initialize datetime structure
    datetime_set_type(&dt, DATETIME_ABSOLUTE, DATETIME_YEAR, DATETIME_SECOND, 0);
    
    // Set date and time
    datetime_set_year(&dt, 2025);
    datetime_set_month(&dt, 8);
    datetime_set_day(&dt, 24);
    
    // Format and display
    char buffer[100];
    if (datetime_format(&dt, buffer) == 0) {
        printf("DateTime: %s\n", buffer);
    }
    
    return 0;
}
```

## API Reference

The library provides functions for:

- **Type management**: `datetime_set_type()`, `datetime_get_type()`
- **Value setting**: `datetime_set_year()`, `datetime_set_month()`, etc.
- **Value getting**: `datetime_get_year()`, `datetime_get_month()`, etc.
- **Formatting**: `datetime_format()`
- **Parsing**: `datetime_scan()`
- **Arithmetic**: `datetime_increment()`, `datetime_difference()`
- **Comparisons**: `datetime_is_same()`, `datetime_is_between()`
- **Time zones**: `datetime_set_timezone()`, `datetime_change_timezone()`

## License

This code is derived from GRASS GIS and maintains the same licensing terms.
