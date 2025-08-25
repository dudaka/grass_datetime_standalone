#!/usr/bin/env python3
"""
Advanced C Header Parser for CFFI cdef() Generation

This script automatically parses C header files and generates
the cdef() string for CFFI bindings.
"""

import os
import re
import sys
from typing import List, Dict, Set

class CHeaderParser:
    """Parse C header files and extract CFFI-compatible declarations"""
    
    def __init__(self):
        self.structs = []
        self.enums = []
        self.constants = []
        self.functions = []
        self.typedefs = []
    
    def clean_c_code(self, content: str) -> str:
        """Remove C comments and preprocessor directives"""
        # Remove /* */ comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        # Remove // comments
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        # Remove #include, #ifndef, etc. (but keep #define)
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#') and not stripped.startswith('#define'):
                continue
            cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)
    
    def extract_structs(self, content: str) -> List[str]:
        """Extract struct definitions"""
        structs = []
        
        # Pattern for typedef struct
        pattern = r'typedef\s+struct\s+(\w+)?\s*\{([^}]+)\}\s*(\w+)\s*;'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for struct_name, struct_body, typedef_name in matches:
            if 'DateTime' in (struct_name or typedef_name):
                # Clean up the struct body
                clean_body = re.sub(r'\s+', ' ', struct_body.strip())
                struct_def = f"typedef struct {typedef_name} {{\n"
                
                # Parse individual fields
                fields = re.findall(r'(\w+(?:\s*\*)?)\s+(\w+)(?:\[.*?\])?;', struct_body)
                for field_type, field_name in fields:
                    struct_def += f"    {field_type.strip()} {field_name};\n"
                
                struct_def += f"}} {typedef_name};"
                structs.append(struct_def)
        
        return structs
    
    def extract_constants(self, content: str) -> List[str]:
        """Extract #define constants"""
        constants = []
        
        # Find #define statements with numeric values
        pattern = r'#define\s+([A-Z_][A-Z0-9_]*)\s+(\d+)'
        matches = re.findall(pattern, content)
        
        for name, value in matches:
            if name.startswith('DATETIME_'):
                constants.append(f"#define {name} {value}")
        
        return constants
    
    def extract_functions(self, content: str) -> List[str]:
        """Extract function declarations"""
        functions = []
        
        # Remove __declspec and other decorators
        content = re.sub(r'__declspec\([^)]+\)', '', content)
        content = re.sub(r'GRASS_DATETIME_EXPORT', '', content)
        
        # Pattern for function declarations
        # Matches: return_type function_name(parameters);
        pattern = r'^\s*([a-zA-Z_][a-zA-Z0-9_\s\*]*?)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*;'
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            
            match = re.match(pattern, line)
            if match:
                return_type, func_name, params = match.groups()
                
                if func_name.startswith('datetime_'):
                    # Clean up the declaration
                    return_type = re.sub(r'\s+', ' ', return_type.strip())
                    params = re.sub(r'\s+', ' ', params.strip())
                    
                    func_decl = f"{return_type} {func_name}({params});"
                    functions.append(func_decl)
        
        return functions
    
    def parse_file(self, filepath: str) -> str:
        """Parse a C header file and return cdef string"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Header file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean the content
        content = self.clean_c_code(content)
        
        # Extract different elements
        self.structs = self.extract_structs(content)
        self.constants = self.extract_constants(content) 
        self.functions = self.extract_functions(content)
        
        return self.generate_cdef()
    
    def generate_cdef(self) -> str:
        """Generate the final cdef string"""
        cdef_parts = []
        
        # Add structs
        if self.structs:
            cdef_parts.append("// Structures")
            cdef_parts.extend(self.structs)
            cdef_parts.append("")
        
        # Add constants
        if self.constants:
            cdef_parts.append("// Constants")
            cdef_parts.extend(self.constants)
            cdef_parts.append("")
        
        # Add functions
        if self.functions:
            cdef_parts.append("// Functions")
            cdef_parts.extend(self.functions)
        
        return '\n'.join(cdef_parts)

def main():
    """Main function for command-line usage"""
    if len(sys.argv) != 2:
        print("Usage: python generate_cdef.py <header_file>")
        print("Example: python generate_cdef.py ../include/grass/datetime.h")
        sys.exit(1)
    
    header_file = sys.argv[1]
    parser = CHeaderParser()
    
    try:
        cdef_string = parser.parse_file(header_file)
        print("Generated cdef string:")
        print("=" * 50)
        print(cdef_string)
        print("=" * 50)
        
        # Optionally save to file
        output_file = "generated_cdef.h"
        with open(output_file, 'w') as f:
            f.write(cdef_string)
        print(f"Saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
