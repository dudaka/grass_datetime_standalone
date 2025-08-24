# Python Wrapper Installation

The Python wrapper for GRASS DateTime library is located in the `python/` directory.

## Quick Install

1. **Build the C library first** (if not already done):
   ```bash
   build.bat  # Windows
   # or
   ./build.sh  # Linux/Unix
   ```

2. **Install Python dependencies**:
   ```bash
   cd python
   pip install -r requirements.txt
   ```

3. **Test the wrapper**:
   ```bash
   python demo.py
   ```

## Development Installation

For development work, install the package in editable mode:

```bash
cd python
pip install -e .
```

This allows you to import the package from anywhere:

```python
from grass_datetime import DateTime
dt = DateTime.absolute(2025, 8, 24, 14, 30, 45)
print(dt)  # "24 Aug 2025 14:30:45"
```

## Package Installation

To install as a regular Python package:

```bash
cd python
pip install .
```

## Files in python/ directory

- `grass_datetime.py` - Main wrapper module
- `test_python_wrapper.py` - Test suite
- `examples.py` - Usage examples
- `demo.py` - Quick demo
- `setup.py` - Package installation script
- `__init__.py` - Package initialization
- `README.md` - Detailed documentation
- `requirements.txt` - Dependencies
- `grass_datetime.dll` - Windows library (copied automatically)

## Troubleshooting

If you get import errors, ensure:
1. The C library is built (`build.bat` or `./build.sh`)
2. CFFI is installed (`pip install cffi`)
3. You're running from the correct directory

See `python/README.md` for complete API documentation.
