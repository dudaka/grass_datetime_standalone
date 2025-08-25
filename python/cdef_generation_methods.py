#!/usr/bin/env python3
"""
Alternative CFFI cdef() Generation Methods

This file shows several different approaches to automatically generate
the cdef() string for CFFI bindings from C header files.
"""

from cffi import FFI
import os
import subprocess
import tempfile

# Method 1: Using the cffi.cdef() with #include (simplest)
def method1_include_header():
    """Use cffi's ability to include headers directly"""
    ffibuilder = FFI()
    
    # This tells CFFI to read the header file directly
    ffibuilder.cdef("""
        #include <grass/datetime.h>
    """, include_dirs=['../include'])
    
    return ffibuilder

# Method 2: Using gcc/clang to preprocess headers
def method2_gcc_preprocess(header_path):
    """Use GCC/Clang to preprocess the header and extract declarations"""
    
    # Use gcc to preprocess the header
    cmd = ['gcc', '-E', '-I../include', header_path]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        preprocessed = result.stdout
        
        # Filter out system headers and keep only our declarations
        lines = preprocessed.split('\n')
        filtered_lines = []
        in_our_header = False
        
        for line in lines:
            if header_path in line and line.startswith('#'):
                in_our_header = True
                continue
            elif line.startswith('#') and not in_our_header:
                continue
            elif line.startswith('#') and in_our_header:
                in_our_header = False
                continue
            
            if in_our_header and line.strip():
                filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

# Method 3: Using pcpp (Pure Python C Preprocessor) - requires: pip install pcpp
def method3_pcpp_preprocess(header_path):
    """Use pcpp to preprocess headers (most accurate)"""
    try:
        from pcpp import Preprocessor
        
        # Create preprocessor instance
        cpp = Preprocessor()
        cpp.add_path('../include')
        
        # Parse the header
        with open(header_path, 'r') as f:
            cpp.parse(f.read(), header_path)
        
        # Get the preprocessed output
        output = []
        cpp.write(output)
        
        return ''.join(output)
        
    except ImportError:
        print("pcpp not available. Install with: pip install pcpp")
        return None

# Method 4: Using pycparser (requires: pip install pycparser)
def method4_pycparser(header_path):
    """Use pycparser to parse C headers (most robust)"""
    try:
        from pycparser import parse_file, c_generator
        
        # Parse the C file
        ast = parse_file(header_path, use_cpp=True, 
                        cpp_args=['-I../include'])
        
        # Generate clean C code
        generator = c_generator.CGenerator()
        return generator.visit(ast)
        
    except ImportError:
        print("pycparser not available. Install with: pip install pycparser")
        return None

# Method 5: Smart regex-based parser (custom implementation)
def method5_smart_parser(header_path):
    """Custom smart parser for C headers"""
    import re
    
    with open(header_path, 'r') as f:
        content = f.read()
    
    # Remove comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    content = re.sub(r'//.*', '', content)
    
    # Remove preprocessor directives except #define
    lines = content.split('\n')
    filtered_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#') and not stripped.startswith('#define'):
            continue
        filtered_lines.append(line)
    content = '\n'.join(filtered_lines)
    
    # Extract meaningful declarations
    declarations = []
    
    # Extract typedef struct
    struct_pattern = r'typedef\s+struct[^{]*\{[^}]+\}\s*\w+\s*;'
    structs = re.findall(struct_pattern, content, re.DOTALL)
    declarations.extend(structs)
    
    # Extract #define constants
    define_pattern = r'#define\s+[A-Z_][A-Z0-9_]*\s+\d+'
    defines = re.findall(define_pattern, content)
    declarations.extend(defines)
    
    # Extract function declarations
    func_pattern = r'^\s*\w+\s+\w+\s*\([^)]*\)\s*;'
    functions = re.findall(func_pattern, content, re.MULTILINE)
    # Filter for datetime functions
    datetime_funcs = [f for f in functions if 'datetime_' in f]
    declarations.extend(datetime_funcs)
    
    return '\n'.join(declarations)

def test_all_methods():
    """Test all methods and show results"""
    header_path = '../include/grass/datetime.h'
    
    if not os.path.exists(header_path):
        print(f"Header file not found: {header_path}")
        return
    
    methods = [
        ("GCC Preprocessing", lambda: method2_gcc_preprocess(header_path)),
        ("PCPP Preprocessing", lambda: method3_pcpp_preprocess(header_path)),
        ("PyCParser", lambda: method4_pycparser(header_path)),
        ("Smart Regex Parser", lambda: method5_smart_parser(header_path)),
    ]
    
    for name, method in methods:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            result = method()
            if result:
                print(result[:500] + "..." if len(result) > 500 else result)
            else:
                print("Method not available or failed")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_all_methods()
