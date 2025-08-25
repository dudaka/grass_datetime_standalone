from cffi import FFI
import os

ffibuilder = FFI()

# ============================================================================
# RECOMMENDED APPROACH: Hybrid Manual + Auto Generation
# ============================================================================

def get_auto_cdef():
    """
    Automatically extract cdef from header file.
    This is the cleanest approach for most projects.
    """
    import re
    
    header_file = '../include/grass/datetime.h'
    
    if not os.path.exists(header_file):
        print(f"❌ Header not found: {header_file}")
        return None
    
    with open(header_file, 'r') as f:
        content = f.read()
    
    print(f"🔍 Auto-generating cdef from: {header_file}")
    
    cdef_parts = []
    
    # 1. Extract DateTime struct (the main one we need)
    struct_pattern = r'typedef\s+struct[^{]*\{([^}]+)\}\s*DateTime\s*;'
    struct_match = re.search(struct_pattern, content, re.DOTALL)
    
    if struct_match:
        struct_body = struct_match.group(1)
        cdef_parts.append(f"typedef struct DateTime {{{struct_body}}} DateTime;")
    
    # 2. Extract DATETIME_* constants  
    const_pattern = r'#define\s+(DATETIME_\w+)\s+(\d+)'
    constants = re.findall(const_pattern, content)
    
    if constants:
        cdef_parts.append("\n// Constants")
        for name, value in constants:
            cdef_parts.append(f"#define {name} {value}")
    
    # 3. Extract datetime_* functions
    # Remove decorators first
    clean_content = re.sub(r'__declspec\([^)]+\)', '', content)
    clean_content = re.sub(r'GRASS_DATETIME_EXPORT', '', clean_content)
    
    func_pattern = r'^\s*([^#\n]*datetime_\w+[^;]*;)'
    functions = re.findall(func_pattern, clean_content, re.MULTILINE)
    
    if functions:
        cdef_parts.append("\n// Functions") 
        for func in functions:
            # Clean up whitespace
            clean_func = ' '.join(func.split())
            if clean_func and not clean_func.startswith('//'):
                cdef_parts.append(clean_func)
    
    result = '\n'.join(cdef_parts)
    print(f"✅ Generated {len(constants)} constants, {len(functions)} functions")
    
    return result

def get_manual_cdef():
    """
    Manual cdef definitions - use this if auto-generation fails
    or if you want precise control over what's included.
    """
    return """
    // DateTime structure
    typedef struct DateTime {
        int mode;
        int from, to;
        int fracsec;
        int year, month, day;
        int hour, minute;
        double second;
        int positive;
        int tz;
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
    
    // Essential functions
    int datetime_set_type(DateTime *dt, int mode, int from, int to, int fracsec);
    int datetime_set_year(DateTime *dt, int year);
    int datetime_set_month(DateTime *dt, int month);
    int datetime_set_day(DateTime *dt, int day);
    int datetime_set_hour(DateTime *dt, int hour);
    int datetime_set_minute(DateTime *dt, int minute);
    int datetime_set_second(DateTime *dt, double second);
    
    int datetime_get_year(const DateTime *dt, int *year);
    int datetime_get_month(const DateTime *dt, int *month);
    int datetime_get_day(const DateTime *dt, int *day);
    int datetime_get_hour(const DateTime *dt, int *hour);
    int datetime_get_minute(const DateTime *dt, int *minute);
    int datetime_get_second(const DateTime *dt, double *second);
    
    int datetime_format(const DateTime *dt, char *buf);
    void datetime_copy(DateTime *src, const DateTime *dst);
    
    int datetime_is_leap_year(int year, int ad);
    int datetime_days_in_month(int year, int month, int ad);
    int datetime_days_in_year(int year, int ad);
    """

# Choose method: Try auto first, fallback to manual
print("🚀 GRASS DateTime CFFI Build")
print("=" * 40)

# Try automatic generation first
cdef_string = get_auto_cdef()

if not cdef_string or len(cdef_string) < 100:
    print("⚠️  Auto-generation failed or incomplete, using manual cdef...")
    cdef_string = get_manual_cdef()
else:
    print("✅ Using auto-generated cdef!")

# Show what we're using
print(f"\n📋 CDEF Preview ({len(cdef_string)} chars):")
print("-" * 50)
preview = cdef_string[:400] + "..." if len(cdef_string) > 400 else cdef_string
print(preview)
print("-" * 50)

# Apply the cdef
ffibuilder.cdef(cdef_string)

# Set source - same as before
ffibuilder.set_source("_grass_datetime_cffi",
"""
     #include <grass/datetime.h>
""",
     libraries=['grass_datetime'],
     library_dirs=['.', '../build', '../build/Release', '../build/Debug'],
     include_dirs=['../include'])

if __name__ == "__main__":
    print("\n🔨 Compiling CFFI extension...")
    ffibuilder.compile(verbose=True)
    print("✅ Build complete!")
