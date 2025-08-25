cmake_minimum_required(VERSION 3.15)
project(GrassDateTimeCFFI VERSION 1.0.0 LANGUAGES C)

# Set C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Add compiler flags for debug/release
if(MSVC)
    set(CMAKE_C_FLAGS_DEBUG "/Od /Zi /MDd")
    set(CMAKE_C_FLAGS_RELEASE "/O2 /DNDEBUG /MD")
else()
    set(CMAKE_C_FLAGS_DEBUG "-g -O0 -Wall -Wextra")
    set(CMAKE_C_FLAGS_RELEASE "-O3 -DNDEBUG")
endif()

# Set default build type to Release if not specified
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

# Collect all source files from lib/datetime
file(GLOB DATETIME_SOURCES "lib/datetime/*.c")

# Option to build shared library (DLL on Windows)
option(BUILD_SHARED_LIB "Build as shared library (DLL)" ON)
option(BUILD_PYTHON_EXTENSION "Build Python CFFI extension" ON)

# Create the datetime library
if(BUILD_SHARED_LIB)
    # Build as shared library
    add_library(grass_datetime SHARED ${DATETIME_SOURCES})
    target_compile_definitions(grass_datetime PRIVATE GRASS_DATETIME_DLL_EXPORT)
    
    # Set output name for DLL
    set_target_properties(grass_datetime PROPERTIES
        OUTPUT_NAME "grass_datetime"
        PREFIX ""
        VERSION 1.0.0
        SOVERSION 1
    )
    
    # Install DLL
    install(TARGETS grass_datetime
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
    )
else()
    # Build as static library
    add_library(grass_datetime STATIC ${DATETIME_SOURCES})
    
    # Install static library
    install(TARGETS grass_datetime
        ARCHIVE DESTINATION lib
    )
endif()

# Install headers
install(FILES 
    ${CMAKE_CURRENT_SOURCE_DIR}/include/grass/datetime.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/grass/defs/datetime.h
    DESTINATION include/grass
)

# Install additional headers
install(DIRECTORY include/grass
    DESTINATION include
    FILES_MATCHING PATTERN "*.h"
)

# Create test executable
add_executable(test_datetime_shared test_datetime.c)
target_link_libraries(test_datetime_shared grass_datetime)

# Enable testing
enable_testing()
add_test(NAME datetime_test COMMAND test_datetime_shared)

# Custom target for Python CFFI extension
if(BUILD_PYTHON_EXTENSION)
    find_program(PYTHON_EXECUTABLE python)
    
    if(PYTHON_EXECUTABLE)
        set(BUILD_SCRIPT ${CMAKE_CURRENT_SOURCE_DIR}/python/grass_datetime_build.py)
        set(TEST_SCRIPT ${CMAKE_CURRENT_SOURCE_DIR}/python/high_level_demo.py)
        
        add_custom_target(python_extension
            COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_FILE:grass_datetime> .
            COMMAND ${PYTHON_EXECUTABLE} ${BUILD_SCRIPT}
            DEPENDS grass_datetime
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            COMMENT "Building Python CFFI extension"
        )
        
        add_custom_target(test_python
            COMMAND ${PYTHON_EXECUTABLE} ${TEST_SCRIPT}
            DEPENDS python_extension
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            COMMENT "Testing Python CFFI extension"
        )
        
        add_custom_target(test_python_direct
            COMMAND ${PYTHON_EXECUTABLE} -B ${CMAKE_CURRENT_SOURCE_DIR}/python/test_direct.py
            DEPENDS python_extension
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            COMMENT "Testing Python CFFI bindings directly"
        )
        
        add_custom_target(test_python_simple
            COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/python/simple_examples.py
            DEPENDS python_extension
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            COMMENT "Running simple Python examples"
        )
        
        add_custom_target(test_python_path
            COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/python/path_demo.py
            DEPENDS python_extension
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            COMMENT "Testing Python DLL path loading"
        )
    else()
        message(WARNING "Python executable not found. Python targets will not be available.")
    endif()
endif()

# Add custom targets for cleanup
add_custom_target(clean_all
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Cleaning all build files"
)

# Display build information
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "Build shared library: ${BUILD_SHARED_LIB}")
message(STATUS "Build Python extension: ${BUILD_PYTHON_EXTENSION}")
message(STATUS "C compiler: ${CMAKE_C_COMPILER}")
message(STATUS "Output directory: ${CMAKE_CURRENT_BINARY_DIR}")
