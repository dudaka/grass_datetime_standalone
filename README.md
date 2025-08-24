# GRASS DateTime Library - Standalone Version

This is a standalone version of the GRASS GIS DateTime library, extracted from the main GRASS project.
It maintains the same structure and functionality as the original GRASS datetime library.

**🐍 Python wrapper available!** See `python/` directory and `PYTHON_INSTALL.md` for Python bindings.

## Directory Structure

```
datetime_standalone/
├── CMakeLists.txt          # Root CMake configuration
├── build.bat               # Windows build script
├── build.sh                # Linux/Unix build script
├── README.md               # This file
├── PYTHON_INSTALL.md       # Python wrapper installation guide
├── python/                 # Python wrapper directory
│   ├── grass_datetime.py   # Main Python wrapper
│   ├── setup.py            # Python package setup
│   ├── demo.py             # Quick demo
│   └── ...                 # Other Python files
├── include/
│   └── grass/
│       ├── datetime.h      # Main DateTime structure and constants
│       └── defs/
│           └── datetime.h  # Function prototypes
└── lib/
    └── datetime/
        ├── CMakeLists.txt   # Library CMake configuration
        ├── README           # Original GRASS documentation
        └── *.c              # All source files
```

## Building the Library

### Windows (with Visual Studio or MinGW):
```bash
build.bat
```

### Linux/Unix:
```bash
chmod +x build.sh
./build.sh
```

### Manual build with CMake:
```bash
mkdir build
cd build
cmake ..
cmake --build .
```

## Source Files

The library consists of 18 C source files:
- between.c    - Utility functions for range checking
- change.c     - DateTime range and precision changes  
- copy.c       - DateTime copying functions
- diff.c       - DateTime difference calculations
- error.c      - Error handling and reporting
- format.c     - DateTime formatting functions
- incr1.c      - DateTime increment operations
- incr2.c      - DateTime increment validation
- incr3.c      - DateTime increment type operations
- local.c      - Local timezone and time functions
- misc.c       - Miscellaneous utilities (leap years, etc.)
- same.c       - DateTime comparison functions
- scan.c       - DateTime parsing from strings
- sign.c       - DateTime sign operations
- type.c       - DateTime type setting and validation
- tz1.c        - Timezone operations
- tz2.c        - Advanced timezone operations
- values.c     - DateTime value operations

## Usage

After building, you will have:
- Static library: `libgrass_datetime.a` (or `.lib` on Windows)
- Shared library: `libgrass_datetime.so` (or `.dll` on Windows)

Include the headers in your C code:
```c
#include <grass/datetime.h>
```

Link with the library:
```bash
gcc -o myprogram myprogram.c -lgrass_datetime -I./include
```

## License

This code is from GRASS GIS and is licensed under the GNU General Public License (GPL) v2 or later.
See the original GRASS project for full license details.
