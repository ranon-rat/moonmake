# Documentación de Moonmake

Moonmake es un sistema de construcción ligero diseñado para proyectos C++, inspirado por makefile, con un enfoque en la simplicidad y facilidad de uso. Proporciona una interfaz basada en Python para gestionar dependencias, compilar código y manejar la construcción de proyectos con soporte para compilación incremental.

## Conceptos Básicos

### Estructura del Proyecto
```
proyecto/
├── .moonmake/
│   ├── bin/          # Binarios compilados
│   ├── obj/          # Archivos objeto
│   ├── lib/          # Bibliotecas generadas
│   └── dependencies/ # Dependencias externas
│       ├── headers/  # Archivos de cabecera
│       └── lib/      # Archivos de biblioteca
├── src/
│   ├── include/      # Archivos de cabecera del proyecto
│   ├── lib/          # Código fuente de bibliotecas
│   └── target/       # Fuentes de ejecutables principales
└── build.py          # Configuración de construcción
```

### Sistema Builder

El sistema Builder gestiona el proceso de compilación a través de reglas que definen cómo se deben construir los archivos y sus dependencias. Soporta compilación incremental usando archivos de dependencias (.d) generados por GCC.

Características principales:
- **Seguimiento automático de dependencias**: Usa archivos .d generados por GCC para rastrear dependencias de headers
- **Construcciones incrementales**: Solo recompila archivos cuando las dependencias de código fuente o headers cambian
- **Soporte para bibliotecas estáticas**: Creación y enlazado automático de bibliotecas
- **Compatibilidad multiplataforma**: Funciona en Windows, Linux y macOS

### Archivos de Dependencias (.d) y Compilación Incremental

Moonmake utiliza la característica de generación de dependencias de GCC para crear archivos `.d` que rastrean qué archivos de cabecera depende cada archivo fuente. Esto permite una compilación incremental inteligente.

#### Cómo funciona:
1. **Generación**: Al compilar con las banderas `-MMD -MP`, GCC crea archivos `.d` junto a los archivos `.o`
2. **Contenido**: Cada archivo `.d` contiene una lista de todos los archivos de cabecera que incluye el archivo fuente
3. **Rastreo**: Moonmake lee estos archivos `.d` para determinar si es necesaria la recompilación
4. **Decisión**: Si cualquier archivo de cabecera es más nuevo que el archivo objeto, ocurre la recompilación

#### Ejemplo de contenido de archivo de dependencias:
```makefile
# main.o.d
main.o: main.cpp \
  src/include/game.h \
  src/include/utils.h \
  .moonmake/dependencies/headers/raylib/raylib.h
```

#### Beneficios:
- **Construcciones rápidas**: Solo se recompilan los archivos cambiados
- **Rastreo preciso**: Captura cambios en archivos de cabecera que afectan la compilación
- **Automático**: No se requiere especificación manual de dependencias

### Comandos Comunes

```bash
# Crear un nuevo proyecto
moonmake-new -n nombre_proyecto

# Instalar dependencias
python build.py install

# Construir el proyecto
python build.py
```

## Referencia de Funciones Básicas

### Funciones de Directorio y Rutas

#### `mmake.get_dir(__file__)`
Retorna la ruta relativa del directorio actual desde la raíz del espacio de trabajo.

#### `mmake.get_extension()`
Retorna la extensión de ejecutable apropiada para la plataforma actual:
- Windows: `.exe`
- Linux/macOS: `""` (sin extensión)

### Gestión de Archivos

#### `mmake.discover(directory, endswith)`
Encuentra recursivamente todos los archivos en un directorio que terminan con una extensión específica. Retorna una lista de rutas relativas.

```python
# Encontrar todos los archivos .cpp en src/lib
cpp_files = mmake.discover("src/lib", ".cpp")
# Resultado: ["main.cpp", "utils/helper.cpp", "math/vector.cpp"]
```

#### `mmake.change_extension(files, new_path, old="", new="")`
Cambia la extensión de los archivos y opcionalmente los mueve a un nuevo directorio. Retorna una lista de nuevas rutas de archivo.

```python
obj_files = mmake.change_extension(
    cpp_files,
    join(dir_path, ".moonmake", "obj"),
    old=".cpp",
    new=".o"
)
# Resultado: [".moonmake/obj/main.o", ".moonmake/obj/utils/helper.o", ".moonmake/obj/math/vector.o"]
```

### Gestión de Dependencias

#### `mmake.download_dependency(url, name, target_dir, headers=["include"])`
Descarga e instala una dependencia externa. No retorna nada, pero configura la dependencia en el directorio destino.

```python
# Ejemplo: Descargar e instalar raylib
mmake.download_dependency(
    "https://github.com/raysan5/raylib/releases/download/5.5/raylib-5.5_win64_mingw-w64.zip",
    "raylib",                # Nombre de la dependencia
    ".moonmake/dependencies", # Dónde instalar
    headers=["include"]      # Qué directorios copiar como cabeceras
)

# Ejemplo: Descargar una biblioteca personalizada
mmake.download_dependency(
    "https://example.com/mibib.zip",
    "mibib",
    ".moonmake/dependencies",
    headers=["include", "src/headers"]  # Múltiples directorios de cabecera
)
```

### Sistema de Construcción

#### `mmake.Builder()`
Crea una nueva instancia del sistema de construcción. El Builder gestiona el proceso de compilación y las dependencias con soporte para construcciones incrementales.

#### `builder.watch(targets, dependencies, command, extra_dependencies=[], show_command=True, dependency_file=False)`
Define una regla de construcción que especifica cómo construir archivos objetivo desde sus dependencias.

**Parámetros:**
- `targets`: Lista de archivos a construir (archivos de salida)
- `dependencies`: Lista de archivos de los que dependen los objetivos (archivos de entrada)
- `command`: Comando de shell a ejecutar (soporta variables especiales)
- `extra_dependencies`: Archivos adicionales a vigilar por cambios
- `show_command`: Si mostrar el comando que se está ejecutando
- `dependency_file`: Habilitar rastreo de archivos .d para construcciones incrementales

**Cuándo usar `dependency_file=True`:**
- Para compilación de C/C++ que genera archivos objeto
- Cuando se usan las banderas de compilador `-MMD -MP`
- Para habilitar rastreo automático de dependencias de headers

#### Variables Especiales en Reglas de Construcción
Al definir reglas de construcción con `builder.watch()`, puedes usar estas variables especiales:
- `$@`: Representa el/los archivo(s) objetivo que se están construyendo
- `$<`: Representa la dependencia en la posición del índice del archivo objetivo (ej., si se está construyendo target[0], $< será dependencies[0])
- `$^`: Representa todas las dependencias (útil para enlazar múltiples archivos)
- `$?`: Representa las dependencias extra (archivos a vigilar por cambios)

#### Proceso de Construcción Incremental
1. **Verificar timestamps**: Compara el tiempo de modificación del archivo objetivo con los archivos de dependencia
2. **Verificar archivos .d**: Si `dependency_file=True`, analiza archivos .d para verificar dependencias de headers
3. **Determinar reconstrucción**: Reconstruye si cualquier dependencia es más nueva que el objetivo
4. **Ejecutar comando**: Ejecuta el comando de construcción solo si es necesaria la reconstrucción

Ejemplos de uso de variables especiales:
```python
# Compilar archivos fuente a objetos con rastreo de dependencias
builder.watch(
    ["main.o", "utils.o"],              # Archivos objeto a construir
    ["main.cpp", "utils.cpp"],          # Archivos fuente
    "g++ -c $< -o $@ -Wall -MMD -MP",   # Compilar con generación de dependencias
    dependency_file=True                # Habilitar rastreo de archivos .d
)

# Enlazar múltiples archivos objeto en ejecutable
builder.watch(
    ["programa.exe"],                   # $@ será "programa.exe"
    ["main.o", "utils.o", "math.o"],   # $^ será "main.o utils.o math.o"
    "g++ $^ -o $@ -lraylib",           # Enlazar todos los objetos
    dependency_file=True                # Rastrear dependencias para enlazado incremental
)

# Crear biblioteca estática desde múltiples objetos
builder.watch(
    ["libmibib.a"],                     # Objetivo de biblioteca estática
    ["obj1.o", "obj2.o", "obj3.o"],    # Dependencias de archivos objeto
    "ar rcs $@ $^"                      # Comando de archivo usando todas las dependencias
)

# Vigilar archivos extra por cambios
builder.watch(
    ["programa.exe"],
    ["main.o"],
    "g++ $< -o $@",
    extra_dependencies=["config.h"],    # Reconstruir si config.h cambia
    dependency_file=True
)
```

### Utilidades

#### `mmake.join_with_flag(paths, flag)`
Une rutas con una bandera específica (ej. `-I` para includes). Retorna una cadena con todas las rutas unidas con la bandera.

```python
INCLUDE_FLAGS = mmake.join_with_flag(include_paths, "-I")
# Resultado: "-I/ruta1 -I/ruta2 -I/ruta3"
```

#### `mmake.strip_lib_prefix(name)`
Elimina el prefijo "lib" de los nombres de bibliotecas. Retorna el nombre de la biblioteca sin el prefijo.

```python
lib_name = mmake.strip_lib_prefix("libraylib.a")
# Resultado: "raylib.a"
```

### Interfaz de Línea de Comandos

#### `mmake.arguments_cmd(sys.argv, execute, install)`
Maneja argumentos de línea de comandos:
- `python build.py`: Ejecuta `execute()`
- `python build.py install`: Ejecuta `install()`

## Ejemplo Completo: Proyecto C++ Multi-Objetivo

Este ejemplo demuestra una configuración completa de construcción para un proyecto C++ con dependencias externas, bibliotecas estáticas y múltiples ejecutables con compilación incremental.

### Estructura del Proyecto
```
proyecto/
├── src/
│   ├── include/          # Headers del proyecto
│   ├── lib/             # Archivos fuente de bibliotecas (.cpp)
│   └── target/          # Archivos fuente de ejecutables (.cpp)
├── .moonmake/
│   ├── obj/             # Archivos objeto generados
│   │   ├── lib/         # Objetos de bibliotecas
│   │   └── target/      # Objetos de objetivos
│   ├── lib/             # Bibliotecas estáticas generadas
│   ├── bin/             # Ejecutables finales
│   └── dependencies/    # Dependencias externas
└── build.py             # Este script de construcción
```

### Script de Construcción Completo

```python
import moonmake as mmake
import platform
import sys

dir_path = mmake.get_dir(__file__)

def join(*dir, separator="/"): 
    return f"{separator}".join(dir)

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
    """Configures and executes the build process with incremental compilation."""
    # Configuración del proyecto
    MOONMAKE_DIR = ".moonmake"
    PROJECT_NAME = "msrc"
    CPP_VERSION = "2b"
    EXTENSION = mmake.get_extension()
    
    # Rutas de include y bibliotecas
    include_paths = [
        join(".", MOONMAKE_DIR, "dependencies", "headers"),
        join(".", dir_path, "src", "include")
    ]
    
    lib_paths = [
        join(MOONMAKE_DIR, "dependencies", "lib"),
        join(MOONMAKE_DIR, "lib")
    ]
    
    # Descubrimiento y enlazado de bibliotecas estáticas
    static_a_files = mmake.discover(join(".", MOONMAKE_DIR, "dependencies", "lib"), ".a")
    static_libs = [f"-l{mmake.strip_lib_prefix(a).replace('.a', '')}" for a in static_a_files]
    
    # Bibliotecas específicas de plataforma
    if platform.system() == "Windows":
        static_libs.extend(["-lgdi32", "-lwinmm"])
    
    # Banderas de compilador y enlazador
    INCLUDE_FLAGS = mmake.join_with_flag(include_paths, "-I")
    LINK_FLAGS = mmake.join_with_flag(lib_paths, "-L")
    STATIC_LIBRARY = " ".join(static_libs)
    COMPILER_FLAGS = f"-Wall -Wextra -std=c++{CPP_VERSION} -Werror -O2"
    IGNORE_FLAGS = "-Wno-unused-parameter -Wno-return-type"  
    OBJ_FLAGS = "-MMD -MP"  # Generar archivos de dependencias (.d) para construcciones incrementales
    
    # Archivos fuente de bibliotecas y compilación de objetos
    lib_files = [f for f in mmake.discover(join(dir_path, "src", "lib"), ".cpp")]
    lib_obj = mmake.change_extension(
        lib_files, 
        join(dir_path, MOONMAKE_DIR, "obj", "lib"), 
        old=".cpp", 
        new=".o"
    )
    lib_static = join(dir_path, MOONMAKE_DIR, "lib", f"lib{PROJECT_NAME}.a")
    
    # Archivos objetivo de ejecutables
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
    
    # Configuración del sistema de construcción
    builder = mmake.Builder()
    
    # Enlazar ejecutables desde archivos objeto
    builder.watch(
        target_bin, 
        target_obj, 
        f"g++ $< -o $@ {COMPILER_FLAGS} {LINK_FLAGS} {STATIC_LIBRARY} -l{PROJECT_NAME}",
        dependency_file=True
    )
    
    # Compilar archivos fuente objetivo a objetos (con rastreo de dependencias)
    builder.watch(
        target_obj, 
        [join(".", "src", "target", f) for f in target_files],
        f"g++ -c $< -o $@ {COMPILER_FLAGS} {INCLUDE_FLAGS} {IGNORE_FLAGS}",
        dependency_file=True
    )
    
    # Crear biblioteca estática desde objetos de biblioteca
    builder.watch(
        [lib_static], 
        lib_obj, 
        "ar rcs $@ $^"
    )
    
    # Compilar archivos fuente de biblioteca a objetos (con rastreo de dependencias)
    builder.watch(
        lib_obj, 
        [join(".", "src", "lib", f) for f in lib_files],
        f"g++ {COMPILER_FLAGS} {IGNORE_FLAGS} -c $< -o $@ {INCLUDE_FLAGS} {OBJ_FLAGS}",
        dependency_file=True
    )
    
    # Ejecutar construcción incremental
    builder.compile_all()

if __name__ == "__main__":
    mmake.arguments_cmd(sys.argv, execute, install)
```

### Características Clave Demostradas

1. **Compilación Incremental**: Usa banderas `-MMD -MP` y `dependency_file=True` para rastrear dependencias de headers
2. **Construcción Multi-objetivo**: Soporta múltiples ejecutables desde diferentes archivos fuente
3. **Creación de Bibliotecas Estáticas**: Construye y enlaza bibliotecas estáticas personalizadas
4. **Dependencias Externas**: Descarga e integra bibliotecas externas (Raylib)
5. **Soporte Multiplataforma**: Maneja automáticamente configuraciones específicas de plataforma

## Soporte de Plataformas

- Windows (MinGW-w64)
- Linux
- macOS