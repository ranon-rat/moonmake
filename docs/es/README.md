# Documentación de Moonmake

Moonmake es un sistema de construcción ligero diseñado para proyectos C++, inspirado por makefile, con un enfoque en la simplicidad y facilidad de uso. Proporciona una interfaz basada en Python para gestionar dependencias, compilar código y manejar la construcción de proyectos.

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

El sistema Builder gestiona el proceso de compilación a través de reglas que definen cómo se deben construir los archivos y sus dependencias.

Características principales:
- Seguimiento automático de dependencias
- Construcciones incrementales
- Soporte para bibliotecas estáticas
- Compatibilidad multiplataforma

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
Crea una nueva instancia del sistema de construcción. El Builder gestiona el proceso de compilación y las dependencias.

#### Variables Especiales en Reglas de Construcción
Al definir reglas de construcción con `builder.watch()`, puedes usar estas variables especiales:
- `$@`: Representa el/los archivo(s) objetivo que se están construyendo
- `$<`: Representa la dependencia en la posición del índice del archivo objetivo (ej., si se está construyendo target[0], $< será dependencies[0])
- `$^`: Representa todas las dependencias (útil para enlazar múltiples archivos)
- `$?`: Representa las dependencias extra (archivos a vigilar por cambios)

Ejemplos de uso de variables especiales:
```python
# Usando $@ y $< para compilación basada en índice
builder.watch(
    ["programa1.exe", "programa2.exe"],  # Objetivos
    ["main1.cpp", "main2.cpp"],         # Dependencias
    "g++ $< -o $@ -Wall"                # Al construir programa1.exe, $< es main1.cpp
                                        # Al construir programa2.exe, $< es main2.cpp
)

# Usando $^ para enlazar múltiples archivos
builder.watch(
    ["programa.exe"],                    # $@ será "programa.exe"
    ["main.o", "utils.o", "math.o"],    # $^ será "main.o utils.o math.o"
    "g++ $^ -o $@ -lraylib"             # Se expande a: g++ main.o utils.o math.o -o programa.exe -lraylib
)

# Usando $? para dependencias extra
builder.watch(
    ["programa.exe"],
    ["main.o"],
    "g++ $< -o $@",
    extra_dependencies=["config.h"]      # $? será "config.h"
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

## Ejemplo de Uso

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
    # Encontrar y procesar archivos fuente
    cpp_files = mmake.discover(join(dir_path, "src"), ".cpp")
    obj_files = mmake.change_extension(
        cpp_files,
        join(dir_path, ".moonmake", "obj"),
        old=".cpp",
        new=".o"
    )
    
    # Configurar construcción
    include_paths = [
        join(".moonmake", "dependencies", "headers"),
        join(dir_path, "src", "include")
    ]
    INCLUDE_FLAGS = mmake.join_with_flag(include_paths, "-I")
    
    # Construir
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

## Soporte de Plataformas

- Windows (MinGW-w64)
- Linux
- macOS