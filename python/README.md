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

## Automatic CFFI cdef() Generation

The CFFI build process requires a `cdef()` string that declares all C types, constants, and functions. Instead of writing this manually, several approaches can automatically generate this from C header files.

### Current Implementation (Hybrid Auto/Manual)

Our `grass_datetime_build.py` uses a smart hybrid approach:

```python
def auto_generate_cdef():
    """Automatically extract cdef from header file with manual fallback"""
    header_file = '../include/grass/datetime.h'
    
    # 1. Extract DateTime struct using regex
    struct_pattern = r'typedef\s+struct[^{]*\{([^}]+)\}\s*DateTime\s*;'
    
    # 2. Extract DATETIME_* constants
    const_pattern = r'#define\s+(DATETIME_\w+)\s+(\d+)'
    
    # 3. Fall back to manual definitions if extraction fails
    if not cdef_parts or no_functions:
        return get_manual_cdef()
```

**✅ Pros:** Simple, reliable, no dependencies, automatic fallback  
**❌ Cons:** May miss complex declarations

### Alternative Approaches

#### 1. Simple Regex Parser
```python
def parse_header_with_regex(header_path):
    with open(header_path, 'r') as f:
        content = f.read()
    
    # Remove comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    content = re.sub(r'//.*', '', content)
    
    # Extract structs
    structs = re.findall(r'typedef\s+struct[^{]*\{[^}]+\}\s*\w+\s*;', content, re.DOTALL)
    
    # Extract constants
    constants = re.findall(r'#define\s+[A-Z_][A-Z0-9_]*\s+\d+', content)
    
    # Extract functions
    functions = re.findall(r'^\s*\w+\s+\w+\s*\([^)]*\)\s*;', content, re.MULTILINE)
    
    return combine_declarations(structs, constants, functions)
```

#### 2. GCC/Clang Preprocessing
```python
def preprocess_with_gcc(header_path):
    """Use GCC to handle all preprocessor directives"""
    cmd = ['gcc', '-E', '-I../include', header_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Filter output to keep only our declarations
    return filter_preprocessed_output(result.stdout)
```

**✅ Pros:** Handles all preprocessor directives correctly  
**❌ Cons:** Requires GCC/Clang installed

#### 3. Pure Python C Preprocessor (pcpp)
```bash
pip install pcpp
```

```python
from pcpp import Preprocessor

def preprocess_with_pcpp(header_path):
    """Most accurate preprocessing in pure Python"""
    cpp = Preprocessor()
    cpp.add_path('../include')
    
    with open(header_path, 'r') as f:
        cpp.parse(f.read(), header_path)
    
    output = []
    cpp.write(output)
    return ''.join(output)
```

**✅ Pros:** Pure Python, very accurate, handles complex headers  
**❌ Cons:** Extra dependency

#### 4. PyCParser (Full C Parsing)
```bash
pip install pycparser
```

```python
from pycparser import parse_file, c_generator

def parse_with_pycparser(header_path):
    """Complete C parsing with AST"""
    ast = parse_file(header_path, use_cpp=True, 
                    cpp_args=['-I../include'])
    
    generator = c_generator.CGenerator()
    return generator.visit(ast)
```

**✅ Pros:** Full C parsing, most robust, handles all C constructs  
**❌ Cons:** Complex, requires proper C preprocessing, large dependency

#### 5. Configuration-Driven Generation
Create `cffi_config.ini`:
```ini
[structures]
DateTime = auto

[constants]
patterns = ["DATETIME_*"]

[functions]  
patterns = ["datetime_*"]
```

```python
def generate_from_config(config_file):
    """Use configuration file to control extraction"""
    config = configparser.ConfigParser()
    config.read(config_file)
    
    # Extract based on patterns and rules
    return extract_declarations_from_config(config)
```

**✅ Pros:** Very flexible, maintainable, version-controllable  
**❌ Cons:** More setup required

### Choosing the Right Approach

| Approach | Complexity | Dependencies | Accuracy | Best For |
|----------|------------|--------------|----------|----------|
| **Hybrid Auto/Manual** | Low | None | Good | Small/medium projects |
| **Regex Parser** | Low | None | Medium | Simple headers |
| **GCC Preprocessing** | Medium | GCC/Clang | High | Complex headers |
| **PCPP** | Medium | pcpp | High | Pure Python needed |
| **PyCParser** | High | pycparser | Highest | Complex C codebases |
| **Configuration** | Medium | None | High | Large projects |

### Implementation Examples

See these files for complete implementations:
- `grass_datetime_build.py` - Current hybrid approach
- `grass_datetime_build_v2.py` - Enhanced version with better extraction
- `generate_cdef.py` - Advanced regex-based parser
- `cdef_generation_methods.py` - Multiple method examples
- `config_cdef_generator.py` - Configuration-driven approach

### Recommendation

For most projects like GRASS DateTime:
1. **Start with hybrid auto/manual** (current approach)
2. **Add pcpp** if headers become complex: `pip install pcpp`
3. **Use configuration-driven** for large projects with many headers
4. **Consider pycparser** only for very complex C codebases

The key is having a reliable manual fallback for when automatic extraction fails.

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
