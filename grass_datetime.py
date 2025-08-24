"""
GRASS DateTime Library Python Wrapper using CFFI

This module provides a Python interface to the GRASS DateTime library,
making it easy to work with dates, times, and time intervals in Python.

Usage:
    from grass_datetime import DateTime, DATETIME_ABSOLUTE, DATETIME_RELATIVE
    
    # Create absolute datetime
    dt = DateTime.absolute(2025, 8, 24, 14, 30, 45.5)
    print(dt.format())  # "24 Aug 2025 14:30:46"
    
    # Create relative datetime (interval)
    interval = DateTime.relative(hours=2, minutes=30)
    print(interval.format())  # "02:30:00"
"""

import os
import sys
from cffi import FFI
from typing import Optional, Union

# Initialize CFFI
ffi = FFI()

# Define C structures and constants from the headers
ffi.cdef("""
    // Constants
    #define DATETIME_ABSOLUTE 1
    #define DATETIME_RELATIVE 2
    #define DATETIME_YEAR     101
    #define DATETIME_MONTH    102
    #define DATETIME_DAY      103
    #define DATETIME_HOUR     104
    #define DATETIME_MINUTE   105
    #define DATETIME_SECOND   106

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

    // Core functions
    int datetime_set_type(DateTime *dt, int mode, int from, int to, int fracsec);
    int datetime_get_type(const DateTime *dt, int *mode, int *from, int *to, int *fracsec);
    
    // Value setting functions
    int datetime_set_year(DateTime *dt, int year);
    int datetime_set_month(DateTime *dt, int month);
    int datetime_set_day(DateTime *dt, int day);
    int datetime_set_hour(DateTime *dt, int hour);
    int datetime_set_minute(DateTime *dt, int minute);
    int datetime_set_second(DateTime *dt, double second);
    
    // Value getting functions
    int datetime_get_year(const DateTime *dt, int *year);
    int datetime_get_month(const DateTime *dt, int *month);
    int datetime_get_day(const DateTime *dt, int *day);
    int datetime_get_hour(const DateTime *dt, int *hour);
    int datetime_get_minute(const DateTime *dt, int *minute);
    int datetime_get_second(const DateTime *dt, double *second);
    
    // Formatting and parsing
    int datetime_format(const DateTime *dt, char *buf);
    int datetime_scan(DateTime *dt, const char *buf);
    
    // Comparison and operations
    int datetime_is_same(const DateTime *src, const DateTime *dst);
    int datetime_difference(const DateTime *a, const DateTime *b, DateTime *result);
    int datetime_increment(DateTime *src, DateTime *incr);
    
    // Timezone operations
    int datetime_set_timezone(DateTime *dt, int minutes);
    int datetime_get_timezone(const DateTime *dt, int *minutes);
    int datetime_change_timezone(DateTime *dt, int minutes);
    int datetime_change_to_utc(DateTime *dt);
    
    // Sign operations
    int datetime_is_positive(const DateTime *dt);
    int datetime_is_negative(const DateTime *dt);
    void datetime_set_positive(DateTime *dt);
    void datetime_set_negative(DateTime *dt);
    
    // Utility functions
    int datetime_days_in_month(int year, int month, int ad);
    int datetime_is_leap_year(int year, int ad);
    int datetime_days_in_year(int year, int ad);
    
    // Error handling
    int datetime_error_code(void);
    char *datetime_error_msg(void);
    void datetime_clear_error(void);
""")

# Load the library
def _load_library():
    """Load the GRASS DateTime shared library."""
    # Try different possible paths - prefer static library on Windows
    possible_paths = [
        "./build/lib/datetime/Release/grass_datetime.lib",  # Windows MSVC static
        "grass_datetime.dll",  # Current directory (Windows)
        "./grass_datetime.dll",  # Current directory explicit
        "./build/lib/datetime/Release/grass_datetime.dll",  # Windows MSVC build
        "./build/lib/datetime/Release/grass_datetime.so",   # Linux
        "./build/lib/datetime/libgrass_datetime.so",       # Alternative Linux
        "./build/lib/datetime/libgrass_datetime.dylib",    # macOS
        "libgrass_datetime.so"  # If in PATH
    ]
    
    for path in possible_paths:
        if os.path.exists(path) or not path.startswith('./'):
            try:
                # For .lib files, try using None to let the system find it
                if path.endswith('.lib'):
                    # Static libraries can't be loaded directly - skip them
                    continue
                return ffi.dlopen(path)
            except OSError as e:
                continue
    
    # If no path works, try without path (system library)
    try:
        return ffi.dlopen("grass_datetime")
    except OSError as e:
        raise RuntimeError(
            f"Could not load GRASS DateTime library. Please ensure it's built and "
            f"available in one of these locations: {', '.join(possible_paths)}\n"
            f"Last error: {e}\n"
            f"Note: On Windows, the DLL may not have exported functions. "
            f"Try rebuilding with proper export declarations."
        )

# Load the library
lib = _load_library()

# Constants
DATETIME_ABSOLUTE = lib.DATETIME_ABSOLUTE
DATETIME_RELATIVE = lib.DATETIME_RELATIVE
DATETIME_YEAR = lib.DATETIME_YEAR
DATETIME_MONTH = lib.DATETIME_MONTH
DATETIME_DAY = lib.DATETIME_DAY
DATETIME_HOUR = lib.DATETIME_HOUR
DATETIME_MINUTE = lib.DATETIME_MINUTE
DATETIME_SECOND = lib.DATETIME_SECOND


class DateTimeError(Exception):
    """Exception raised for GRASS DateTime library errors."""
    
    def __init__(self, message: str = None):
        if message is None:
            error_code = lib.datetime_error_code()
            if error_code != 0:
                error_msg_ptr = lib.datetime_error_msg()
                if error_msg_ptr != ffi.NULL:
                    message = ffi.string(error_msg_ptr).decode('utf-8', errors='ignore')
                else:
                    message = f"DateTime error code: {error_code}"
            else:
                message = "Unknown DateTime error"
        super().__init__(message)


class DateTime:
    """
    Python wrapper for GRASS DateTime structure.
    
    Provides a convenient interface for working with absolute and relative dates/times.
    """
    
    def __init__(self):
        """Initialize a new DateTime object."""
        self._dt = ffi.new("DateTime *")
        lib.datetime_clear_error()
    
    @classmethod
    def absolute(cls, year: int = None, month: int = None, day: int = None,
                 hour: int = None, minute: int = None, second: float = None,
                 timezone_minutes: int = None) -> 'DateTime':
        """
        Create an absolute DateTime.
        
        Args:
            year: Year (e.g., 2025)
            month: Month (1-12)
            day: Day (1-31)
            hour: Hour (0-23)
            minute: Minute (0-59)
            second: Second (0.0-59.999...)
            timezone_minutes: Timezone offset in minutes from UTC
            
        Returns:
            DateTime: New absolute DateTime object
        """
        dt = cls()
        
        # Determine range based on provided values
        from_unit = DATETIME_YEAR
        to_unit = DATETIME_YEAR
        
        if month is not None:
            to_unit = DATETIME_MONTH
        if day is not None:
            to_unit = DATETIME_DAY
        if hour is not None:
            to_unit = DATETIME_HOUR
        if minute is not None:
            to_unit = DATETIME_MINUTE
        if second is not None:
            to_unit = DATETIME_SECOND
        
        # Set type
        if lib.datetime_set_type(dt._dt, DATETIME_ABSOLUTE, from_unit, to_unit, 0) != 0:
            raise DateTimeError()
        
        # Set values
        if year is not None:
            if lib.datetime_set_year(dt._dt, year) != 0:
                raise DateTimeError(f"Invalid year: {year}")
        if month is not None:
            if lib.datetime_set_month(dt._dt, month) != 0:
                raise DateTimeError(f"Invalid month: {month}")
        if day is not None:
            if lib.datetime_set_day(dt._dt, day) != 0:
                raise DateTimeError(f"Invalid day: {day}")
        if hour is not None:
            if lib.datetime_set_hour(dt._dt, hour) != 0:
                raise DateTimeError(f"Invalid hour: {hour}")
        if minute is not None:
            if lib.datetime_set_minute(dt._dt, minute) != 0:
                raise DateTimeError(f"Invalid minute: {minute}")
        if second is not None:
            if lib.datetime_set_second(dt._dt, second) != 0:
                raise DateTimeError(f"Invalid second: {second}")
        
        # Set timezone if provided
        if timezone_minutes is not None:
            if lib.datetime_set_timezone(dt._dt, timezone_minutes) != 0:
                raise DateTimeError(f"Invalid timezone: {timezone_minutes}")
        
        return dt
    
    @classmethod
    def relative(cls, years: int = 0, months: int = 0, days: int = 0,
                 hours: int = 0, minutes: int = 0, seconds: float = 0.0) -> 'DateTime':
        """
        Create a relative DateTime (time interval).
        
        Args:
            years: Number of years
            months: Number of months
            days: Number of days
            hours: Number of hours
            minutes: Number of minutes
            seconds: Number of seconds
            
        Returns:
            DateTime: New relative DateTime object
        """
        dt = cls()
        
        # Determine range based on non-zero values
        from_unit = DATETIME_SECOND
        to_unit = DATETIME_SECOND
        
        if years != 0:
            from_unit = DATETIME_YEAR
        elif months != 0:
            from_unit = DATETIME_MONTH
        elif days != 0:
            from_unit = DATETIME_DAY
        elif hours != 0:
            from_unit = DATETIME_HOUR
        elif minutes != 0:
            from_unit = DATETIME_MINUTE
        
        # Set to the highest unit that has a value
        if years != 0:
            to_unit = DATETIME_YEAR
        elif months != 0:
            to_unit = DATETIME_MONTH
        elif days != 0:
            to_unit = DATETIME_DAY
        elif hours != 0:
            to_unit = DATETIME_HOUR
        elif minutes != 0:
            to_unit = DATETIME_MINUTE
        
        # Set type
        if lib.datetime_set_type(dt._dt, DATETIME_RELATIVE, from_unit, to_unit, 0) != 0:
            raise DateTimeError()
        
        # Only set non-zero values to avoid "Invalid years: 0" errors
        if years != 0:
            if lib.datetime_set_year(dt._dt, years) != 0:
                raise DateTimeError(f"Invalid years: {years}")
        if months != 0:
            if lib.datetime_set_month(dt._dt, months) != 0:
                raise DateTimeError(f"Invalid months: {months}")
        if days != 0:
            if lib.datetime_set_day(dt._dt, days) != 0:
                raise DateTimeError(f"Invalid days: {days}")
        if hours != 0:
            if lib.datetime_set_hour(dt._dt, hours) != 0:
                raise DateTimeError(f"Invalid hours: {hours}")
        if minutes != 0:
            if lib.datetime_set_minute(dt._dt, minutes) != 0:
                raise DateTimeError(f"Invalid minutes: {minutes}")
        if seconds != 0.0:
            if lib.datetime_set_second(dt._dt, seconds) != 0:
                raise DateTimeError(f"Invalid seconds: {seconds}")
        
        return dt
    
    @classmethod
    def parse(cls, date_string: str) -> 'DateTime':
        """
        Parse a date/time string into a DateTime object.
        
        Args:
            date_string: String representation of date/time
            
        Returns:
            DateTime: Parsed DateTime object
        """
        dt = cls()
        date_bytes = date_string.encode('utf-8')
        
        if lib.datetime_scan(dt._dt, date_bytes) != 0:
            raise DateTimeError(f"Could not parse date string: {date_string}")
        
        return dt
    
    def format(self) -> str:
        """
        Format the DateTime as a string.
        
        Returns:
            str: Formatted date/time string
        """
        buffer = ffi.new("char[]", 1000)
        if lib.datetime_format(self._dt, buffer) != 0:
            raise DateTimeError("Could not format DateTime")
        
        return ffi.string(buffer).decode('utf-8', errors='ignore').strip()
    
    def __str__(self) -> str:
        """String representation of the DateTime."""
        return self.format()
    
    def __repr__(self) -> str:
        """Detailed representation of the DateTime."""
        try:
            formatted = self.format()
            mode = "absolute" if self.is_absolute() else "relative"
            return f"DateTime({mode}: '{formatted}')"
        except:
            return "DateTime(<invalid>)"
    
    # Property accessors
    @property
    def year(self) -> Optional[int]:
        """Get the year component."""
        year = ffi.new("int *")
        if lib.datetime_get_year(self._dt, year) == 0:
            return year[0]
        return None
    
    @year.setter
    def year(self, value: int):
        """Set the year component."""
        if lib.datetime_set_year(self._dt, value) != 0:
            raise DateTimeError(f"Invalid year: {value}")
    
    @property
    def month(self) -> Optional[int]:
        """Get the month component."""
        month = ffi.new("int *")
        if lib.datetime_get_month(self._dt, month) == 0:
            return month[0]
        return None
    
    @month.setter
    def month(self, value: int):
        """Set the month component."""
        if lib.datetime_set_month(self._dt, value) != 0:
            raise DateTimeError(f"Invalid month: {value}")
    
    @property
    def day(self) -> Optional[int]:
        """Get the day component."""
        day = ffi.new("int *")
        if lib.datetime_get_day(self._dt, day) == 0:
            return day[0]
        return None
    
    @day.setter
    def day(self, value: int):
        """Set the day component."""
        if lib.datetime_set_day(self._dt, value) != 0:
            raise DateTimeError(f"Invalid day: {value}")
    
    @property
    def hour(self) -> Optional[int]:
        """Get the hour component."""
        hour = ffi.new("int *")
        if lib.datetime_get_hour(self._dt, hour) == 0:
            return hour[0]
        return None
    
    @hour.setter
    def hour(self, value: int):
        """Set the hour component."""
        # Check if we need to expand the datetime range to include hours
        current_to = getattr(self._dt, 'to')
        if current_to < DATETIME_HOUR:
            # Expand the range to include hours
            current_from = getattr(self._dt, 'from')
            if lib.datetime_set_type(self._dt, self._dt.mode, current_from, DATETIME_HOUR, 0) != 0:
                raise DateTimeError("Could not expand datetime range to include hours")
        
        if lib.datetime_set_hour(self._dt, value) != 0:
            raise DateTimeError(f"Invalid hour: {value}")
    
    @property
    def minute(self) -> Optional[int]:
        """Get the minute component."""
        minute = ffi.new("int *")
        if lib.datetime_get_minute(self._dt, minute) == 0:
            return minute[0]
        return None
    
    @minute.setter
    def minute(self, value: int):
        """Set the minute component."""
        # Check if we need to expand the datetime range to include minutes
        current_to = getattr(self._dt, 'to')
        if current_to < DATETIME_MINUTE:
            # Expand the range to include minutes
            current_from = getattr(self._dt, 'from')
            if lib.datetime_set_type(self._dt, self._dt.mode, current_from, DATETIME_MINUTE, 0) != 0:
                raise DateTimeError("Could not expand datetime range to include minutes")
        
        if lib.datetime_set_minute(self._dt, value) != 0:
            raise DateTimeError(f"Invalid minute: {value}")
    
    @property
    def second(self) -> Optional[float]:
        """Get the second component."""
        second = ffi.new("double *")
        if lib.datetime_get_second(self._dt, second) == 0:
            return second[0]
        return None
    
    @second.setter
    def second(self, value: float):
        """Set the second component."""
        # Check if we need to expand the datetime range to include seconds
        current_to = getattr(self._dt, 'to')
        if current_to < DATETIME_SECOND:
            # Expand the range to include seconds
            current_from = getattr(self._dt, 'from')
            if lib.datetime_set_type(self._dt, self._dt.mode, current_from, DATETIME_SECOND, 0) != 0:
                raise DateTimeError("Could not expand datetime range to include seconds")
        
        if lib.datetime_set_second(self._dt, value) != 0:
            raise DateTimeError(f"Invalid second: {value}")
    
    @property
    def timezone_minutes(self) -> Optional[int]:
        """Get the timezone offset in minutes."""
        tz = ffi.new("int *")
        if lib.datetime_get_timezone(self._dt, tz) == 0:
            return tz[0]
        return None
    
    @timezone_minutes.setter
    def timezone_minutes(self, value: int):
        """Set the timezone offset in minutes."""
        if lib.datetime_set_timezone(self._dt, value) != 0:
            raise DateTimeError(f"Invalid timezone: {value}")
    
    # Comparison and operations
    def is_same(self, other: 'DateTime') -> bool:
        """Check if this DateTime is the same as another."""
        return lib.datetime_is_same(self._dt, other._dt) != 0
    
    def __eq__(self, other) -> bool:
        """Check equality with another DateTime."""
        if not isinstance(other, DateTime):
            return False
        return self.is_same(other)
    
    def difference(self, other: 'DateTime') -> 'DateTime':
        """Calculate the difference between two DateTimes."""
        result = DateTime()
        if lib.datetime_difference(self._dt, other._dt, result._dt) != 0:
            raise DateTimeError("Could not calculate difference")
        return result
    
    def __sub__(self, other: 'DateTime') -> 'DateTime':
        """Subtract another DateTime from this one."""
        return self.difference(other)
    
    def add(self, interval: 'DateTime') -> 'DateTime':
        """Add a time interval to this DateTime."""
        # Create a copy
        result = DateTime()
        result._dt.mode = self._dt.mode
        setattr(result._dt, 'from', getattr(self._dt, 'from'))
        result._dt.to = self._dt.to
        result._dt.fracsec = self._dt.fracsec
        result._dt.year = self._dt.year
        result._dt.month = self._dt.month
        result._dt.day = self._dt.day
        result._dt.hour = self._dt.hour
        result._dt.minute = self._dt.minute
        result._dt.second = self._dt.second
        result._dt.positive = self._dt.positive
        result._dt.tz = self._dt.tz
        
        if lib.datetime_increment(result._dt, interval._dt) != 0:
            raise DateTimeError("Could not add interval")
        return result
    
    def __add__(self, other: 'DateTime') -> 'DateTime':
        """Add another DateTime (interval) to this one."""
        return self.add(other)
    
    # Type checking
    def is_absolute(self) -> bool:
        """Check if this is an absolute DateTime."""
        return self._dt.mode == DATETIME_ABSOLUTE
    
    def is_relative(self) -> bool:
        """Check if this is a relative DateTime (interval)."""
        return self._dt.mode == DATETIME_RELATIVE
    
    def is_positive(self) -> bool:
        """Check if this DateTime has a positive sign."""
        return lib.datetime_is_positive(self._dt) != 0
    
    def is_negative(self) -> bool:
        """Check if this DateTime has a negative sign."""
        return lib.datetime_is_negative(self._dt) != 0
    
    def set_positive(self):
        """Set this DateTime to positive."""
        lib.datetime_set_positive(self._dt)
    
    def set_negative(self):
        """Set this DateTime to negative."""
        lib.datetime_set_negative(self._dt)
    
    # Timezone operations
    def to_utc(self):
        """Convert this DateTime to UTC."""
        if lib.datetime_change_to_utc(self._dt) != 0:
            raise DateTimeError("Could not convert to UTC")
    
    def change_timezone(self, timezone_minutes: int):
        """Change the timezone of this DateTime."""
        if lib.datetime_change_timezone(self._dt, timezone_minutes) != 0:
            raise DateTimeError(f"Could not change timezone to {timezone_minutes}")


# Utility functions
def days_in_month(year: int, month: int) -> int:
    """Get the number of days in a given month and year."""
    return lib.datetime_days_in_month(year, month, 1)  # 1 for AD (Anno Domini)

def is_leap_year(year: int) -> bool:
    """Check if a year is a leap year."""
    return lib.datetime_is_leap_year(year, 1) != 0  # 1 for AD

def days_in_year(year: int) -> int:
    """Get the number of days in a given year."""
    return lib.datetime_days_in_year(year, 1)  # 1 for AD


# Version information
__version__ = "1.0.0"
__author__ = "GRASS DateTime Library Python Wrapper"
__description__ = "Python wrapper for GRASS GIS DateTime library using CFFI"
