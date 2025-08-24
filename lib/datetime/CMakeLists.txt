cmake_minimum_required(VERSION 3.10)
project(grass_datetime VERSION 1.0 LANGUAGES C)

# Set include directories
include_directories(../../include)

# Source files
set(SOURCES
    between.c change.c copy.c diff.c error.c format.c
    incr1.c incr2.c incr3.c local.c misc.c same.c
    scan.c sign.c type.c tz1.c tz2.c values.c
)

# Create static library
add_library(grass_datetime_static STATIC ${SOURCES})
set_target_properties(grass_datetime_static PROPERTIES OUTPUT_NAME grass_datetime)

# Create shared library
add_library(grass_datetime_shared SHARED ${SOURCES})
set_target_properties(grass_datetime_shared PROPERTIES OUTPUT_NAME grass_datetime)

# Set compiler flags for Release builds only
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_options(grass_datetime_static PRIVATE /O2)
    target_compile_options(grass_datetime_shared PRIVATE /O2)
endif()
