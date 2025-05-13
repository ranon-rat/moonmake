# Moonmake Documentation

Moonmake is a lightweight build system designed for C++ projects, with a focus on simplicity and ease of use. It provides a Python-based interface for managing dependencies, compiling code, and handling project builds.

## Core Concepts

### Project Structure
A typical moonmake project follows this structure:
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

The Builder system is the core of moonmake. It manages the compilation process through a set of rules that define how files should be built and their dependencies.

Key features:
- Automatic dependency tracking
- Incremental builds
- Support for static libraries
- Cross-platform compatibility

#### Basic Builder Usage

```python
builder = mmake.Builder()

# Rule to compile a target
builder.watch(
    target_files,      # Files to build
    dependencies,      # Required dependencies
    compile_command,   # Command to execute
    extra_dependencies # Additional dependencies to watch
)
```

### Common Commands

1. **Creating a New Project**
```bash
python -m moonmake.create -n project_name
```

2. **Installing Dependencies**
```bash
python build.py install
```

3. **Building the Project**
```bash
python build.py
```

### Build Configuration

The `build.py` file is where you configure your project. Here's a basic example:

```python
def execute():
    # Configure paths and flags
    include_paths = [...]
    lib_paths = [...]
    
    # Set up compiler flags
    COMPILER_FLAGS = "-Wall -Wextra -std=c++2b"
    
    # Create builder
    builder = mmake.Builder()
    
    # Add build rules
    builder.watch(target_files, dependencies, compile_command)
    
    # Execute build
    builder.compile_all()
```

### Dependency Management

Moonmake includes a simple dependency management system:

```python
def install():
    mmake.download_dependency(
        url,           # Dependency URL
        name,         # Dependency name
        target_dir,   # Installation directory
        headers=["include"]  # Header directories to copy
    )
```

### Special Variables in Commands

When writing build commands, you can use these special variables:
- `$@` : The target file
- `$<` : The first dependency
- `$^` : All dependencies
- `$?` : Extra dependencies

## Best Practices

1. **Project Organization**
   - Keep header files in `src/include`
   - Place library code in `src/lib`
   - Put main executables in `src/target`

2. **Dependencies**
   - Use the `install()` function to manage external dependencies
   - Keep dependency versions in sync using the link system

3. **Build Rules**
   - Use appropriate compiler flags for your project
   - Include necessary system libraries (e.g., `-lgdi32` for Windows)
   - Watch for changes in header files

## Platform Support

Moonmake supports:
- Windows (MinGW-w64)
- Linux
- macOS

Each platform has specific configurations handled automatically by the build system.

## Core Functions Reference

This section explains the basic functions provided by moonmake that you'll commonly use in your `build.py` file.

### Directory and Path Functions

#### `mmake.get_dir(__file__)`
```python
dir_path = mmake.get_dir(__file__)
```
Returns the relative path of the current directory from the workspace root. This is useful for creating paths relative to your build script.

#### `mmake.get_extension()`
```python
EXTENSION = mmake.get_extension()
```
Returns the appropriate executable extension for the current platform:
- Windows: `.exe`
- Linux: `""` (no extension)
- macOS: `""` (no extension)

### File Discovery and Management

#### `mmake.discover(directory, endswith)`
```python
headers = mmake.discover(join(dir_path, "src", "include"), ".h++")
```
Recursively finds all files in a directory that end with a specific extension. Returns a list of relative paths.

Example:
```python
# Find all .cpp files in src/lib
cpp_files = mmake.discover("src/lib", ".cpp")
# Result: ["main.cpp", "utils/helper.cpp", ...]
```

#### `mmake.change_extension(files, new_path, old="", new="")`
```python
obj_files = mmake.change_extension(
    cpp_files,
    join(dir_path, ".moonmake", "obj"),
    old=".cpp",
    new=".o"
)
```
Changes the extension of a list of files and optionally moves them to a new directory. Useful for generating object file paths from source files.

### Dependency Management

#### `mmake.download_dependency(url, name, target_dir, headers=["include"])`
```python
mmake.download_dependency(
    "https://example.com/lib.zip",
    "mylib",
    ".moonmake/dependencies",
    headers=["include"]
)
```
Downloads and installs an external dependency. It:
- Downloads the dependency from the URL
- Extracts it to the target directory
- Copies header files from specified directories
- Manages version tracking through a link file

### Path and Flag Utilities

#### `mmake.join_with_flag(paths, flag)`
```python
INCLUDE_FLAGS = mmake.join_with_flag(include_paths, "-I")
# Result: "-I/path1 -I/path2 -I/path3"
```
Joins a list of paths with a specific flag. Commonly used for generating compiler flags like `-I` for includes or `-L` for library paths.

#### `mmake.strip_lib_prefix(name)`
```python
lib_name = mmake.strip_lib_prefix("libraylib.a")
# Result: "raylib.a"
```
Removes the "lib" prefix from library names. Useful when generating linker flags.

### Build System Functions

#### `mmake.Builder()`
```python
builder = mmake.Builder()
```
Creates a new build system instance. This is the main class you'll use to define build rules.

#### `builder.watch(target, dependencies, command, extra_dependencies=[])`
```python
builder.watch(
    target_files,          # Files to build
    dependency_files,      # Required dependencies
    "g++ $< -o $@",       # Build command
    extra_dependencies     # Additional files to watch
)
```
Defines a build rule. The command can use special variables:
- `$@`: Target file
- `$<`: First dependency
- `$^`: All dependencies
- `$?`: Extra dependencies

#### `builder.compile_all()`
```python
builder.compile_all()
```
Executes all build rules in the correct order, respecting dependencies.

### Command Line Interface

#### `mmake.arguments_cmd(sys.argv, execute, install)`
```python
if __name__ == "__main__":
    mmake.arguments_cmd(sys.argv, execute, install)
```
Handles command-line arguments for your build script. Supports:
- `python build.py`: Runs the `execute()` function
- `python build.py install`: Runs the `install()` function

### Example Usage

Here's a complete example showing how these functions work together:

```python
import moonmake as mmake
from os.path import join
import platform
import sys

dir_path = mmake.get_dir(__file__)

def install():
    # Download and install raylib
    raylib_url = "https://github.com/raysan5/raylib/releases/download/5.5/raylib-5.5_win64_mingw-w64.zip"
    mmake.download_dependency(
        raylib_url,
        "raylib",
        ".moonmake/dependencies",
        headers=["include"]
    )

def execute():
    # Find all source files
    cpp_files = mmake.discover(join(dir_path, "src"), ".cpp")
    
    # Generate object file paths
    obj_files = mmake.change_extension(
        cpp_files,
        join(dir_path, ".moonmake", "obj"),
        old=".cpp",
        new=".o"
    )
    
    # Set up include paths
    include_paths = [
        join(".moonmake", "dependencies", "headers"),
        join(dir_path, "src", "include")
    ]
    INCLUDE_FLAGS = mmake.join_with_flag(include_paths, "-I")
    
    # Create and configure builder
    builder = mmake.Builder()
    
    # Add build rules
    builder.watch(
        obj_files,
        cpp_files,
        f"g++ -c $< -o $@ -Wall -Wextra {INCLUDE_FLAGS}"
    )
    
    # Execute build
    builder.compile_all()

if __name__ == "__main__":
    mmake.arguments_cmd(sys.argv, execute, install) 
```