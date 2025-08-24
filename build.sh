#!/bin/bash
echo "Building GRASS DateTime Library..."

mkdir -p build
cd build

echo "Configuring with CMake..."
cmake ..

echo "Building..."
make

echo "Build completed!"
echo "Static library: build/lib/datetime/libgrass_datetime.a"
echo "Shared library: build/lib/datetime/libgrass_datetime.so"
