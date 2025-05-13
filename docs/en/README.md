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
Recursively finds all files in a directory that end with a specific extension. Returns a list of relative paths.

```python
# Find all .cpp files in src/lib
cpp_files = mmake.discover("src/lib", ".cpp")
# Result: ["main.cpp", "utils/helper.cpp", "math/vector.cpp"]
```

#### `mmake.change_extension(files, new_path, old="", new="")`
Changes the extension of files and optionally moves them to a new directory. Returns a list of new file paths.

```python
obj_files = mmake.change_extension(
    cpp_files,
    join(dir_path, ".moonmake", "obj"),
    old=".cpp",
    new=".o"
)
# Result: [".moonmake/obj/main.o", ".moonmake/obj/utils/helper.o", ".moonmake/obj/math/vector.o"]
```

### Dependency Management

#### `mmake.download_dependency(url, name, target_dir, headers=["include"])`
Downloads and installs an external dependency. Returns nothing, but sets up the dependency in the target directory.

```python
# Example: Download and install raylib
mmake.download_dependency(
    "https://github.com/raysan5/raylib/releases/download/5.5/raylib-5.5_win64_mingw-w64.zip",
    "raylib",                # Name of the dependency
    ".moonmake/dependencies", # Where to install
    headers=["include"]      # Which directories to copy as headers
)

# Example: Download a custom library
mmake.download_dependency(
    "https://example.com/mylib.zip",
    "mylib",
    ".moonmake/dependencies",
    headers=["include", "src/headers"]  # Multiple header directories
)
```

### Build System

#### `mmake.Builder()`
Creates a new build system instance. The Builder manages the compilation process and dependencies.

#### Special Variables in Build Rules
When defining build rules with `builder.watch()`, you can use these special variables:
- `$@`: Represents the target file(s) being built
- `$<`: Represents the dependency at the index position of the target file (e.g., if target[0] is being built, $< will be dependencies[0])
- `$^`: Represents all dependencies (useful for linking multiple files)
- `$?`: Represents extra dependencies (files to watch for changes)

Examples of using special variables:
```python
# Using $@ and $< for index-based compilation
builder.watch(
    ["program1.exe", "program2.exe"],    # Targets
    ["main1.cpp", "main2.cpp"],         # Dependencies
    "g++ $< -o $@ -Wall"                # When building program1.exe, $< is main1.cpp
                                        # When building program2.exe, $< is main2.cpp
)

# Using $^ for linking multiple files
builder.watch(
    ["program.exe"],                    # $@ will be "program.exe"
    ["main.o", "utils.o", "math.o"],   # $^ will be "main.o utils.o math.o"
    "g++ $^ -o $@ -lraylib"            # Expands to: g++ main.o utils.o math.o -o program.exe -lraylib
)

# Using $? for extra dependencies
builder.watch(
    ["program.exe"],
    ["main.o"],
    "g++ $< -o $@",
    extra_dependencies=["config.h"]     # $? will be "config.h"
)
```

### Utilities

#### `mmake.join_with_flag(paths, flag)`
Joins paths with a specific flag (e.g., `-I` for includes). Returns a string with all paths joined with the flag.

```python
INCLUDE_FLAGS = mmake.join_with_flag(include_paths, "-I")
# Result: "-I/path1 -I/path2 -I/path3"
```

#### `mmake.strip_lib_prefix(name)`
Removes the "lib" prefix from library names. Returns the library name without the prefix.

```python
lib_name = mmake.strip_lib_prefix("libraylib.a")
# Result: "raylib.a"
```

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