#!/usr/bin/env python3
"""
Configuration-driven CFFI cdef() generator

This approach uses a configuration file to define what to extract
from C headers, making it very flexible and maintainable.
"""

import configparser
import os
import re
import fnmatch
from typing import List, Dict

class ConfigurableCdefGenerator:
    """Generate cdef() strings based on configuration file"""
    
    def __init__(self, config_file: str = 'cffi_config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
    
    def extract_from_headers(self) -> str:
        """Extract declarations based on configuration"""
        cdef_parts = []
        
        # Get header files to process
        header_files = self.config.get('headers', 'files').strip('[]').replace("'", "").replace('"', '').split(',')
        header_files = [f.strip() for f in header_files]
        
        for header_file in header_files:
            if not os.path.exists(header_file):
                print(f"⚠️  Header file not found: {header_file}")
                continue
                
            print(f"📁 Processing: {header_file}")
            
            with open(header_file, 'r') as f:
                content = f.read()
            
            # Extract structures
            if 'structures' in self.config:
                structs = self.extract_structures(content)
                if structs:
                    cdef_parts.extend(structs)
            
            # Extract constants
            if 'constants' in self.config:
                constants = self.extract_constants(content)
                if constants:
                    cdef_parts.append("\n// Constants")
                    cdef_parts.extend(constants)
            
            # Extract functions  
            if 'functions' in self.config:
                functions = self.extract_functions(content)
                if functions:
                    cdef_parts.append("\n// Functions")
                    cdef_parts.extend(functions)
        
        return '\n'.join(cdef_parts)
    
    def extract_structures(self, content: str) -> List[str]:
        """Extract structure definitions"""
        structs = []
        
        # Get structure names to extract
        struct_config = dict(self.config['structures'])
        
        for struct_name, extract_mode in struct_config.items():
            if extract_mode == 'auto':
                # Automatically extract struct
                pattern = rf'typedef\s+struct[^{{]*\{{([^}}]+)\}}\s*{struct_name}\s*;'
                match = re.search(pattern, content, re.DOTALL)
                
                if match:
                    struct_body = match.group(1)
                    structs.append(f"typedef struct {struct_name} {{{struct_body}}} {struct_name};")
                    print(f"✅ Extracted struct: {struct_name}")
        
        return structs
    
    def extract_constants(self, content: str) -> List[str]:
        """Extract constants based on patterns"""
        constants = []
        
        # Get patterns
        patterns_str = self.config.get('constants', 'patterns', fallback='[]')
        patterns = eval(patterns_str)  # Simple eval for list
        
        for pattern in patterns:
            # Convert shell pattern to regex
            regex_pattern = pattern.replace('*', r'\w*')
            matches = re.findall(rf'#define\s+({regex_pattern})\s+(\d+)', content)
            
            for name, value in matches:
                constants.append(f"#define {name} {value}")
        
        print(f"✅ Extracted {len(constants)} constants")
        return constants
    
    def extract_functions(self, content: str) -> List[str]:
        """Extract function declarations based on patterns"""
        functions = []
        
        # Get patterns
        patterns_str = self.config.get('functions', 'patterns', fallback='[]')
        patterns = eval(patterns_str)  # Simple eval for list
        
        for pattern in patterns:
            # Convert shell pattern to regex
            func_prefix = pattern.replace('*', '')
            
            # Look for function declarations
            func_pattern = rf'^\s*(?:\w+\s+)*(\w+\s+{func_prefix}\w+\s*\([^)]*\))\s*;'
            matches = re.findall(func_pattern, content, re.MULTILINE)
            
            for match in matches:
                clean_func = re.sub(r'\s+', ' ', match.strip())
                functions.append(f"{clean_func};")
        
        # Add manual functions if specified
        if self.config.has_option('functions', 'manual_functions'):
            manual_funcs_str = self.config.get('functions', 'manual_functions')
            manual_funcs = eval(manual_funcs_str)  # Simple eval for list
            functions.extend(manual_funcs)
        
        print(f"✅ Extracted {len(functions)} functions")
        return functions

def generate_cdef_from_config(config_file: str = 'cffi_config.ini') -> str:
    """Generate cdef string using configuration file"""
    if not os.path.exists(config_file):
        print(f"⚠️  Config file not found: {config_file}")
        return ""
    
    generator = ConfigurableCdefGenerator(config_file)
    return generator.extract_from_headers()

if __name__ == "__main__":
    # Test the configuration-based approach
    cdef_string = generate_cdef_from_config()
    
    print("\n" + "="*60)
    print("GENERATED CDEF STRING:")
    print("="*60)
    print(cdef_string)
    print("="*60)
