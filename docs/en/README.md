# Moonmake Documentation

Moonmake is a lightweight build system designed for C++ projects inspired by makefile, with a focus on simplicity and ease of use. It provides a Python-based interface for managing dependencies, compiling code, and handling project builds.

## Core Concepts

### Project Structure
```
project/
├── .moonmake/
│   ├── bin/          # Compiled binaries
│   ├── obj/          # Object files
│   ├── lib/          # Generated libraries
│   └── dependencies/ # External dependencies
│       ├── headers/  # Header files
│       └── lib/      # Library files
├── src/
│   ├── include/      # Project header files
│   ├── lib/          # Library source files
│   └── target/       # Main executable sources
└── build.py          # Build configuration
```

### Builder System

The Builder system manages the compilation process through rules that define how files should be built and their dependencies.

Key features:
- Automatic dependency tracking
- Incremental builds
- Support for static libraries
- Cross-platform compatibility

### Common Commands

```bash
# Create a new project
moonmake-new -n project_name

# Install dependencies
python build.py install

# Build the project
python build.py
```

## Core Functions Reference

### Directory and Path Functions

#### `mmake.get_dir(__file__)`
Returns the relative path of the current directory from the workspace root.

#### `mmake.get_extension()`
Returns the appropriate executable extension for the current platform:
- Windows: `.exe`
- Linux/macOS: `""` (no extension)

### File Management

#### `mmake.discover(directory, endswith)`
Recursively finds all files in a directory that end with a specific extension.

```python
# Find all .cpp files in src/lib
cpp_files = mmake.discover("src/lib", ".cpp")
```

#### `mmake.change_extension(files, new_path, old="", new="")`
Changes the extension of files and optionally moves them to a new directory.

```python
obj_files = mmake.change_extension(
    cpp_files,
    join(dir_path, ".moonmake", "obj"),
    old=".cpp",
    new=".o"
)
```

### Dependency Management

#### `mmake.download_dependency(url, name, target_dir, headers=["include"])`
Downloads and installs an external dependency:
- Downloads from URL
- Extracts to target directory
- Copies header files
- Manages version tracking

### Build System

#### `mmake.Builder()`
Creates a new build system instance.

#### `builder.watch(target, dependencies, command, extra_dependencies=[])`
Defines a build rule using special variables:
- `$@`: Target file
- `$<`: Dependency of the index of the target file
- `$^`: All dependencies
- `$?`: Extra dependencies

#### `builder.compile_all()`
Executes all build rules in the correct order.

### Utilities

#### `mmake.join_with_flag(paths, flag)`
Joins paths with a specific flag (e.g., `-I` for includes).

#### `mmake.strip_lib_prefix(name)`
Removes the "lib" prefix from library names.

### Command Line Interface

#### `mmake.arguments_cmd(sys.argv, execute, install)`
Handles command-line arguments:
- `python build.py`: Runs `execute()`
- `python build.py install`: Runs `install()`

## Example Usage

```python
import moonmake as mmake
from os.path import join
import platform
import sys

dir_path = mmake.get_dir(__file__)

def install():
    raylib_url = "https://github.com/raysan5/raylib/releases/download/5.5/raylib-5.5_win64_mingw-w64.zip"
    mmake.download_dependency(
        raylib_url,
        "raylib",
        ".moonmake/dependencies",
        headers=["include"]
    )

def execute():
    # Find and process source files
    cpp_files = mmake.discover(join(dir_path, "src"), ".cpp")
    obj_files = mmake.change_extension(
        cpp_files,
        join(dir_path, ".moonmake", "obj"),
        old=".cpp",
        new=".o"
    )
    
    # Configure build
    include_paths = [
        join(".moonmake", "dependencies", "headers"),
        join(dir_path, "src", "include")
    ]
    INCLUDE_FLAGS = mmake.join_with_flag(include_paths, "-I")
    
    # Build
    builder = mmake.Builder()
    builder.watch(
        obj_files,
        cpp_files,
        f"g++ -c $< -o $@ -Wall -Wextra {INCLUDE_FLAGS}"
    )
    builder.compile_all()

if __name__ == "__main__":
    mmake.arguments_cmd(sys.argv, execute, install)
```

## Platform Support

- Windows (MinGW-w64)
- Linux
- macOS