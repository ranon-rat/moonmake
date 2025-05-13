import moonmake as mmake
from os.path import join
import platform
import sys

dir_path = mmake.get_dir(__file__)

def get_raylib_url():
    """Determines the Raylib download URL based on the operating system."""
    system = platform.system()
    BASE_URL = "https://github.com/raysan5/raylib/releases/download/5.5"
    
    if system == "Windows":
        return f"{BASE_URL}/raylib-5.5_win64_mingw-w64.zip"
    elif system == "Darwin":  # macOS
        return f"{BASE_URL}/raylib-5.5_macos.tar.gz"
    elif system == "Linux":
        return f"{BASE_URL}/raylib-5.5_linux_amd64.tar.gz"
    else:
        raise Exception(f"Unsupported system: {system}")

def install():
    """Downloads and installs the necessary dependencies."""
    raylib_url = get_raylib_url()
    mmake.download_dependency(
        raylib_url, 
        "raylib", 
        ".moonmake/dependencies", 
        headers=["include"]
    )

def execute():
    """Configures and executes the build process."""
    # Directories and configuration
    MOONMAKE_DIR = ".moonmake"
    PROJECT_NAME = "msrc"
    CPP_VERSION = "2b"
    EXTENSION = mmake.get_extension()
    
    # Important paths
    include_paths = [
        join(".", MOONMAKE_DIR, "dependencies", "headers"),
        join(".", dir_path, "src", "include")
    ]
    
    lib_paths = [
        join(MOONMAKE_DIR, "dependencies", "lib"),
        join( MOONMAKE_DIR, "lib")
    ]
    
    # Header files
    headers = [join(dir_path, "src", "include", f) 
               for f in mmake.discover(join(dir_path, "src", "include"), ".h++")]
    
    # Static libraries
    static_a_files = mmake.discover(join(".", MOONMAKE_DIR, "dependencies", "lib"), ".a")
    static_libs = [f"-l{mmake.strip_lib_prefix(a).replace('.a', '')}" for a in static_a_files]
    
    if platform.system() == "Windows":
        static_libs.extend(["-lgdi32", "-lwinmm"])
    
    # Compilation flags
    INCLUDE_FLAGS = mmake.join_with_flag(include_paths, "-I")
    LINK_FLAGS = mmake.join_with_flag(lib_paths, "-L")
    STATIC_LIBRARY = " ".join(static_libs)
    COMPILER_FLAGS = f"-Wall -Wextra -std=c++{CPP_VERSION}"
    IGNORE_FLAGS = "-Wno-unused-parameter -Wno-type-limits"
    
    # Files to watch for changes
    static_watch_files = [join(MOONMAKE_DIR, "dependencies", "lib", a) for a in static_a_files]
    
    # Library files
    lib_files = [f for f in mmake.discover(join(dir_path, "src", "lib"), ".cpp")]
    lib_obj = mmake.change_extension(
        lib_files, 
        join(dir_path, MOONMAKE_DIR, "obj", "lib"), 
        old=".cpp", 
        new=".o"
    )
    lib_static = join(dir_path, MOONMAKE_DIR, "lib", f"lib{PROJECT_NAME}.a")
    
    # Target files (binaries)
    target_files = [f for f in mmake.discover(join(dir_path, "src", "target"), ".cpp")]
    target_obj = mmake.change_extension(
        target_files, 
        join(dir_path, MOONMAKE_DIR, "obj", "target"), 
        old=".cpp", 
        new=".o"
    )
    target_bin = mmake.change_extension(
        target_files, 
        join(dir_path, MOONMAKE_DIR, "bin"), 
        old=".cpp", 
        new=EXTENSION
    )
    
    # Configure the builder
    builder = mmake.Builder()
    
    # Rule to generate the final binaries
    builder.watch(
        target_bin, 
        target_obj, 
        f"g++ $< -o $@ {COMPILER_FLAGS} {LINK_FLAGS} {STATIC_LIBRARY} -l{PROJECT_NAME}",
        extra_dependencies=[lib_static, *static_watch_files, *headers]
    )
    
    # Rule to compile target object files
    builder.watch(
        target_obj, 
        [join(".", "src", "target", f) for f in target_files],
        f"g++ -c $< -o $@ {COMPILER_FLAGS} {INCLUDE_FLAGS} {IGNORE_FLAGS}",
        extra_dependencies=[lib_static, *static_watch_files, *headers]
    )
    
    # Rule to create the static library
    builder.watch(
        [lib_static], 
        lib_obj, 
        "ar rcs $@ $^"
    )
    
    # Rule to compile library object files
    builder.watch(
        lib_obj, 
        [join(".", "src", "lib", f) for f in lib_files],
        f"g++ {COMPILER_FLAGS} {IGNORE_FLAGS} -c $< -o $@ {INCLUDE_FLAGS}",
        extra_dependencies=[*headers]
    )
    
    # Execute all build rules
    builder.compile_all()

if __name__ == "__main__":
    mmake.arguments_cmd(sys.argv, execute, install)