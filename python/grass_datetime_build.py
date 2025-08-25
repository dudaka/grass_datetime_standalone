from cffi import FFI
import os
import re

ffibuilder = FFI()

def auto_generate_cdef():
    """
    Automatically generate cdef from header file.
    This is the recommended approach for your project.
    """
    header_file = '../include/grass/datetime.h'
    
    if not os.path.exists(header_file):
        print(f"Header file not found: {header_file}")
        print("Using manual fallback definitions...")
        return get_manual_cdef()
    
    print(f"Parsing header file: {header_file}")
    
    with open(header_file, 'r') as f:
        content = f.read()
    
    # Extract what we need for CFFI
    cdef_parts = []
    
    # 1. Extract DateTime struct
    struct_match = re.search(r'typedef\s+struct[^{]*\{([^}]+)\}\s*DateTime\s*;', content, re.DOTALL)
    if struct_match:
        struct_body = struct_match.group(1)
        cdef_parts.append(f"typedef struct DateTime {{{struct_body}}} DateTime;")
        print("SUCCESS: Found DateTime struct")
    
    # 2. Extract constants
    constants = re.findall(r'#define\s+(DATETIME_\w+)\s+(\d+)', content)
    if constants:
        cdef_parts.append("\n// Constants")
        for name, value in constants:
            cdef_parts.append(f"#define {name} {value}")
        print(f"SUCCESS: Found {len(constants)} constants")
    
    # 3. Extract function declarations 
    # Look for functions that start with datetime_ 
    func_pattern = r'^\s*(?:__declspec\([^)]+\)\s+)?(?:GRASS_DATETIME_EXPORT\s+)?(\w+\s+datetime_\w+\s*\([^)]*\))\s*;'
    functions = re.findall(func_pattern, content, re.MULTILINE)
    
    if functions:
        cdef_parts.append("\n// Functions")
        for func in functions:
            # Clean up the function declaration
            clean_func = re.sub(r'\s+', ' ', func.strip())
            cdef_parts.append(f"{clean_func};")
        print(f"SUCCESS: Found {len(functions)} functions")
    else:
        print("WARNING: No functions found with regex, trying alternative extraction...")
        # Try alternative pattern
        alt_pattern = r'(int|void|char\s*\*)\s+(datetime_\w+)\s*\([^)]*\)'
        alt_functions = re.findall(alt_pattern, content, re.MULTILINE)
        
        if alt_functions:
            cdef_parts.append("\n// Functions") 
            for return_type, func_name in alt_functions:
                # We need to get the full function signature
                full_pattern = rf'{return_type}\s+{func_name}\s*\([^)]*\)\s*;'
                full_match = re.search(full_pattern, content, re.MULTILINE)
                if full_match:
                    clean_func = ' '.join(full_match.group(0).split())
                    cdef_parts.append(clean_func)
            print(f"SUCCESS: Found {len(alt_functions)} functions with alternative method")
    
    if not cdef_parts:
        print("WARNING: No declarations found, using manual fallback...")
        return get_manual_cdef()
    
    # Check if we got functions - if not, use manual fallback with functions
    has_functions = any("datetime_" in part and "(" in part for part in cdef_parts)
    if not has_functions:
        print("WARNING: No functions extracted, using manual fallback...")
        return get_manual_cdef()
    
    result = '\n'.join(cdef_parts)
    print("SUCCESS: Successfully generated cdef from header!")
    return result

def get_manual_cdef():
    """Manual cdef definitions as fallback"""
    return """
    // DateTime structure
    typedef struct DateTime {
        int mode;      // absolute or relative
        int from, to;
        int fracsec;   // #decimal place in printed seconds
        int year, month, day;
        int hour, minute;
        double second;
        int positive;
        int tz;        // timezone - minutes from UTC
    } DateTime;
    
    // Constants
    #define DATETIME_ABSOLUTE 1
    #define DATETIME_RELATIVE 2
    #define DATETIME_YEAR     101
    #define DATETIME_MONTH    102
    #define DATETIME_DAY      103
    #define DATETIME_HOUR     104
    #define DATETIME_MINUTE   105
    #define DATETIME_SECOND   106
    
    // Core functions that definitely exist
    int datetime_set_type(DateTime *dt, int mode, int from, int to, int fracsec);
    int datetime_set_year(DateTime *dt, int year);
    int datetime_set_month(DateTime *dt, int month);
    int datetime_set_day(DateTime *dt, int day);
    int datetime_set_hour(DateTime *dt, int hour);
    int datetime_set_minute(DateTime *dt, int minute);
    int datetime_set_second(DateTime *dt, double second);
    
    // Getters
    int datetime_get_year(const DateTime *dt, int *year);
    int datetime_get_month(const DateTime *dt, int *month);
    int datetime_get_day(const DateTime *dt, int *day);
    int datetime_get_hour(const DateTime *dt, int *hour);
    int datetime_get_minute(const DateTime *dt, int *minute);
    int datetime_get_second(const DateTime *dt, double *second);
    
    // Formatting
    int datetime_format(const DateTime *dt, char *buf);
    
    // Copy function
    void datetime_copy(DateTime *src, const DateTime *dst);
    
    // Utility functions
    int datetime_is_leap_year(int year, int ad);
    int datetime_days_in_month(int year, int month, int ad);
    int datetime_days_in_year(int year, int ad);
    """

# Generate the cdef string automatically
cdef_string = auto_generate_cdef()
print("\nUsing cdef string:")
print("-" * 50)
print(cdef_string[:300] + "..." if len(cdef_string) > 300 else cdef_string)
print("-" * 50)

ffibuilder.cdef(cdef_string)
ffibuilder.set_source("_grass_datetime_cffi",
"""
     #include <grass/datetime.h>   // the C header of the library
""",
     libraries=['grass_datetime'],           # library name, for the linker (looks for grass_datetime.dll)
     library_dirs=['.', '../build', '../build/Release', '../build/Debug'],  # look for library in build directories
     include_dirs=['../include'])     # look for headers

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
