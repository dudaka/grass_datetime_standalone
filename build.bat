@echo off
echo Building GRASS DateTime Library...

if not exist build mkdir build
cd build

echo Configuring with CMake...
cmake ..

echo Building...
cmake --build .

echo Build completed!
echo Static library: build/lib/datetime/libgrass_datetime.a
echo Shared library: build/lib/datetime/libgrass_datetime.dll (Windows) or libgrass_datetime.so (Linux)

pause
