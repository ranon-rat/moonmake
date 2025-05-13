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
Encuentra recursivamente todos los archivos en un directorio que terminan con una extensión específica.

```python
# Encontrar todos los archivos .cpp en src/lib
cpp_files = mmake.discover("src/lib", ".cpp")
```

#### `mmake.change_extension(files, new_path, old="", new="")`
Cambia la extensión de los archivos y opcionalmente los mueve a un nuevo directorio.

```python
obj_files = mmake.change_extension(
    cpp_files,
    join(dir_path, ".moonmake", "obj"),
    old=".cpp",
    new=".o"
)
```

### Gestión de Dependencias

#### `mmake.download_dependency(url, name, target_dir, headers=["include"])`
Descarga e instala una dependencia externa:
- Descarga desde URL
- Extrae al directorio destino
- Copia archivos de cabecera
- Gestiona seguimiento de versiones

### Sistema de Construcción

#### `mmake.Builder()`
Crea una nueva instancia del sistema de construcción.

#### `builder.watch(target, dependencies, command, extra_dependencies=[])`
Define una regla de construcción usando variables especiales:
- `$@`: Archivo objetivo
- `$<`: Dependencia del índice del archivo objetivo
- `$^`: Todas las dependencias
- `$?`: Dependencias extra

#### `builder.compile_all()`
Ejecuta todas las reglas de construcción en el orden correcto.

### Utilidades

#### `mmake.join_with_flag(paths, flag)`
Une rutas con una bandera específica (ej. `-I` para includes).

#### `mmake.strip_lib_prefix(name)`
Elimina el prefijo "lib" de los nombres de bibliotecas.

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