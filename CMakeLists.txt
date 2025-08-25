cmake_minimum_required(VERSION 3.10)
project(grass_datetime VERSION 1.0.0 LANGUAGES C)

# Set C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/include)

# Collect all source files from lib/datetime
file(GLOB DATETIME_SOURCES "lib/datetime/*.c")

# Create shared library
add_library(grass_datetime SHARED ${DATETIME_SOURCES})

# Set compile definitions for DLL export on Windows
target_compile_definitions(grass_datetime PRIVATE GRASS_DATETIME_DLL_EXPORT)

# Set target properties
set_target_properties(grass_datetime PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
    PUBLIC_HEADER "include/grass/datetime.h;include/grass/defs/datetime.h"
)

# On Windows, set the output name to avoid lib prefix
if(WIN32)
    set_target_properties(grass_datetime PROPERTIES
        OUTPUT_NAME "grass_datetime"
        WINDOWS_EXPORT_ALL_SYMBOLS ON
    )
endif()

# Create test executable
add_executable(test_datetime_shared test_datetime.c)

# Link the test executable with the shared library
target_link_libraries(test_datetime_shared grass_datetime)

# Install targets
install(TARGETS grass_datetime
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    PUBLIC_HEADER DESTINATION include/grass
)

# Install additional headers
install(DIRECTORY include/grass
    DESTINATION include
    FILES_MATCHING PATTERN "*.h"
)

# Add test
enable_testing()
add_test(NAME datetime_test COMMAND test_datetime_shared)
