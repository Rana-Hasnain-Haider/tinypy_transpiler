@echo off
if "%1"=="" (
    echo Usage: compile_tpy.bat path\to\filename.tpy
    echo Example: compile_tpy.bat hello.tpy
    exit /b 1
)

set input_file=%~1
set base_name=%~n1
set full_dir=%~dp1
set py_file=%full_dir%%base_name%.py

echo Compiling %input_file% with tinypy compiler...
python tinypy_compiler.py "%input_file%"

if errorlevel 1 (
    echo Error: Python compilation failed
    exit /b 1
)

echo Compiling C code and linking...
gcc main.c -IC:/Users/hasnain/AppData/Local/Programs/Python/Python313/include -LC:/Users/hasnain/AppData/Local/Programs/Python/Python313/libs -lpython313 -o "%base_name%.exe"

if errorlevel 1 (
    echo Error: GCC compilation failed
    exit /b 1
)

echo Successfully created %base_name%.exe

echo Running %base_name%.exe with %py_file%...
echo ================================
"%base_name%.exe" "%py_file%"
echo ================================
echo Program execution completed.
