"""
GRASS DateTime Python Wrapper

A Python interface to the GRASS DateTime C library using CFFI.
"""

import os
from typing import Optional, Tuple, Union

# Add DLL directory before importing CFFI module
_dll_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'build', 'Release'))
if os.path.exists(_dll_directory):
    os.add_dll_directory(_dll_directory)

try:
    import _grass_datetime_cffi as _cffi_module
    ffi = _cffi_module.ffi
    lib = _cffi_module.lib
except ImportError as e:
    raise ImportError(f"Failed to import CFFI module. Make sure the C library is built and the DLL is available. Error: {e}") from e

class DateTimeError(Exception):
    """Exception raised for DateTime library errors."""
    pass

class DateTime:
    """
    Python wrapper for GRASS DateTime structure.
    
    Provides a Pythonic interface to the C DateTime library.
    """
    
    # Constants
    ABSOLUTE = lib.DATETIME_ABSOLUTE
    RELATIVE = lib.DATETIME_RELATIVE
    
    YEAR = lib.DATETIME_YEAR
    MONTH = lib.DATETIME_MONTH
    DAY = lib.DATETIME_DAY
    HOUR = lib.DATETIME_HOUR
    MINUTE = lib.DATETIME_MINUTE
    SECOND = lib.DATETIME_SECOND
    
    def __init__(self, mode: int = None, from_unit: int = None, to_unit: int = None, fracsec: int = 0):
        """
        Initialize a DateTime object.
        
        Args:
            mode: ABSOLUTE or RELATIVE
            from_unit: Starting time unit (YEAR, MONTH, DAY, HOUR, MINUTE, SECOND)
            to_unit: Ending time unit
            fracsec: Number of decimal places for seconds
        """
        self._dt = ffi.new("DateTime *")
        
        if mode is not None and from_unit is not None and to_unit is not None:
            self.set_type(mode, from_unit, to_unit, fracsec)
    
    def _check_error(self):
        """Check for errors and raise exception if any."""
        error_code = lib.datetime_error_code()
        if error_code != 0:
            error_msg = ffi.string(lib.datetime_error_msg()).decode('utf-8')
            lib.datetime_clear_error()
            raise DateTimeError(f"DateTime error {error_code}: {error_msg}")
    
    def set_type(self, mode: int, from_unit: int, to_unit: int, fracsec: int = 0) -> None:
        """Set the type of the DateTime object."""
        result = lib.datetime_set_type(self._dt, mode, from_unit, to_unit, fracsec)
        if result != 0:
            self._check_error()
    
    def get_type(self) -> Tuple[int, int, int, int]:
        """Get the type of the DateTime object."""
        mode = ffi.new("int *")
        from_unit = ffi.new("int *")
        to_unit = ffi.new("int *")
        fracsec = ffi.new("int *")
        
        result = lib.datetime_get_type(self._dt, mode, from_unit, to_unit, fracsec)
        if result != 0:
            self._check_error()
            
        return mode[0], from_unit[0], to_unit[0], fracsec[0]
    
    # Property setters
    def set_year(self, year: int) -> None:
        """Set the year."""
        result = lib.datetime_set_year(self._dt, year)
        if result != 0:
            self._check_error()
    
    def set_month(self, month: int) -> None:
        """Set the month (1-12)."""
        result = lib.datetime_set_month(self._dt, month)
        if result != 0:
            self._check_error()
    
    def set_day(self, day: int) -> None:
        """Set the day of month (1-31)."""
        result = lib.datetime_set_day(self._dt, day)
        if result != 0:
            self._check_error()
    
    def set_hour(self, hour: int) -> None:
        """Set the hour (0-23)."""
        result = lib.datetime_set_hour(self._dt, hour)
        if result != 0:
            self._check_error()
    
    def set_minute(self, minute: int) -> None:
        """Set the minute (0-59)."""
        result = lib.datetime_set_minute(self._dt, minute)
        if result != 0:
            self._check_error()
    
    def set_second(self, second: float) -> None:
        """Set the second (0-59.999...)."""
        result = lib.datetime_set_second(self._dt, second)
        if result != 0:
            self._check_error()
    
    # Property getters
    def get_year(self) -> int:
        """Get the year."""
        year = ffi.new("int *")
        result = lib.datetime_get_year(self._dt, year)
        if result != 0:
            self._check_error()
        return year[0]
    
    def get_month(self) -> int:
        """Get the month."""
        month = ffi.new("int *")
        result = lib.datetime_get_month(self._dt, month)
        if result != 0:
            self._check_error()
        return month[0]
    
    def get_day(self) -> int:
        """Get the day."""
        day = ffi.new("int *")
        result = lib.datetime_get_day(self._dt, day)
        if result != 0:
            self._check_error()
        return day[0]
    
    def get_hour(self) -> int:
        """Get the hour."""
        hour = ffi.new("int *")
        result = lib.datetime_get_hour(self._dt, hour)
        if result != 0:
            self._check_error()
        return hour[0]
    
    def get_minute(self) -> int:
        """Get the minute."""
        minute = ffi.new("int *")
        result = lib.datetime_get_minute(self._dt, minute)
        if result != 0:
            self._check_error()
        return minute[0]
    
    def get_second(self) -> float:
        """Get the second."""
        second = ffi.new("double *")
        result = lib.datetime_get_second(self._dt, second)
        if result != 0:
            self._check_error()
        return second[0]
    
    # Python properties for convenient access
    @property
    def year(self) -> int:
        return self.get_year()
    
    @year.setter
    def year(self, value: int):
        self.set_year(value)
    
    @property
    def month(self) -> int:
        return self.get_month()
    
    @month.setter
    def month(self, value: int):
        self.set_month(value)
    
    @property
    def day(self) -> int:
        return self.get_day()
    
    @day.setter
    def day(self, value: int):
        self.set_day(value)
    
    @property
    def hour(self) -> int:
        return self.get_hour()
    
    @hour.setter
    def hour(self, value: int):
        self.set_hour(value)
    
    @property
    def minute(self) -> int:
        return self.get_minute()
    
    @minute.setter
    def minute(self, value: int):
        self.set_minute(value)
    
    @property
    def second(self) -> float:
        return self.get_second()
    
    @second.setter
    def second(self, value: float):
        self.set_second(value)
    
    # Utility methods
    def format(self) -> str:
        """Format the DateTime as a string."""
        buffer = ffi.new("char[]", 256)
        result = lib.datetime_format(self._dt, buffer)
        if result != 0:
            self._check_error()
        return ffi.string(buffer).decode('utf-8')
    
    def parse(self, datetime_string: str) -> None:
        """Parse a datetime string."""
        result = lib.datetime_scan(self._dt, datetime_string.encode('utf-8'))
        if result != 0:
            self._check_error()
    
    def is_same(self, other: 'DateTime') -> bool:
        """Check if this DateTime is the same as another."""
        return lib.datetime_is_same(self._dt, other._dt) != 0
    
    def is_absolute(self) -> bool:
        """Check if this is an absolute DateTime."""
        return lib.datetime_is_absolute(self._dt) != 0
    
    def is_relative(self) -> bool:
        """Check if this is a relative DateTime."""
        return lib.datetime_is_relative(self._dt) != 0
    
    def is_positive(self) -> bool:
        """Check if this DateTime is positive."""
        return lib.datetime_is_positive(self._dt) != 0
    
    def is_negative(self) -> bool:
        """Check if this DateTime is negative."""
        return lib.datetime_is_negative(self._dt) != 0
    
    def set_timezone(self, minutes: int) -> None:
        """Set timezone offset in minutes from UTC."""
        result = lib.datetime_set_timezone(self._dt, minutes)
        if result != 0:
            self._check_error()
    
    def get_timezone(self) -> int:
        """Get timezone offset in minutes from UTC."""
        minutes = ffi.new("int *")
        result = lib.datetime_get_timezone(self._dt, minutes)
        if result != 0:
            self._check_error()
        return minutes[0]
    
    def __str__(self) -> str:
        """String representation of the DateTime."""
        try:
            return self.format()
        except DateTimeError:
            return f"DateTime(unformatted)"
    
    def __repr__(self) -> str:
        """Representation of the DateTime."""
        try:
            mode, from_unit, to_unit, fracsec = self.get_type()
            return f"DateTime(mode={mode}, from={from_unit}, to={to_unit}, fracsec={fracsec})"
        except DateTimeError:
            return "DateTime(uninitialized)"

# Utility functions
def days_in_month(year: int, month: int, ad: int = 1) -> int:
    """Get the number of days in a month."""
    return lib.datetime_days_in_month(year, month, ad)

def is_leap_year(year: int, ad: int = 1) -> bool:
    """Check if a year is a leap year."""
    return lib.datetime_is_leap_year(year, ad) != 0

def days_in_year(year: int, ad: int = 1) -> int:
    """Get the number of days in a year."""
    return lib.datetime_days_in_year(year, ad)

# Constants for easy access
ABSOLUTE = DateTime.ABSOLUTE
RELATIVE = DateTime.RELATIVE
YEAR = DateTime.YEAR
MONTH = DateTime.MONTH
DAY = DateTime.DAY
HOUR = DateTime.HOUR
MINUTE = DateTime.MINUTE
SECOND = DateTime.SECOND
