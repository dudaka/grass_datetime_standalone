from cffi import FFI

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
    
    // Core functions
    int datetime_set_type(DateTime *dt, int mode, int from, int to, int fracsec);
    int datetime_get_type(const DateTime *dt, int *mode, int *from, int *to, int *fracsec);
    
    // Value setters
    int datetime_set_year(DateTime *dt, int year);
    int datetime_set_month(DateTime *dt, int month);
    int datetime_set_day(DateTime *dt, int day);
    int datetime_set_hour(DateTime *dt, int hour);
    int datetime_set_minute(DateTime *dt, int minute);
    int datetime_set_second(DateTime *dt, double second);
    
    // Value getters
    int datetime_get_year(const DateTime *dt, int *year);
    int datetime_get_month(const DateTime *dt, int *month);
    int datetime_get_day(const DateTime *dt, int *day);
    int datetime_get_hour(const DateTime *dt, int *hour);
    int datetime_get_minute(const DateTime *dt, int *minute);
    int datetime_get_second(const DateTime *dt, double *second);
    
    // Formatting and parsing
    int datetime_format(const DateTime *dt, char *buf);
    int datetime_scan(DateTime *dt, const char *buf);
    
    // Utility functions
    int datetime_is_same(const DateTime *src, const DateTime *dst);
    int datetime_difference(const DateTime *a, const DateTime *b, DateTime *result);
    int datetime_increment(DateTime *src, DateTime *incr);
    
    // Error handling
    int datetime_error_code(void);
    char *datetime_error_msg(void);
    void datetime_clear_error(void);
    
    // Timezone functions
    int datetime_set_timezone(DateTime *dt, int minutes);
    int datetime_get_timezone(const DateTime *dt, int *minutes);
    int datetime_change_timezone(DateTime *dt, int minutes);
    
    // Validation functions
    int datetime_is_absolute(const DateTime *dt);
    int datetime_is_relative(const DateTime *dt);
    int datetime_is_positive(const DateTime *dt);
    int datetime_is_negative(const DateTime *dt);
    
    // Utility functions
    int datetime_days_in_month(int year, int month, int ad);
    int datetime_is_leap_year(int year, int ad);
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
