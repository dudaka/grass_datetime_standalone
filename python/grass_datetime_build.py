from cffi import FFI
import os

ffibuilder = FFI()

# cdef() expects a single string declaring the C types, functions and
# globals needed to use the shared object. It must be in valid C syntax.
ffibuilder.cdef("""
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
""")

# For shared library approach, we'll link against the DLL
ffibuilder.set_source("_grass_datetime_cffi",
"""
     #include <grass/datetime.h>   // the C header of the library
""",
     libraries=['grass_datetime'],           # library name, for the linker (looks for grass_datetime.dll)
     library_dirs=['.', '../build', '../build/Release', '../build/Debug'],  # look for library in build directories
     include_dirs=['../include'])     # look for headers

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
