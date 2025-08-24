@echo off
echo Compiling test program with MSVC...
cl /I.\include test_datetime.c .\build\lib\datetime\Release\grass_datetime.lib /Fe:test_datetime.exe
echo.
if exist test_datetime.exe (
    echo Test program compiled successfully!
    echo Run: test_datetime.exe
) else (
    echo Compilation failed!
)
pause
