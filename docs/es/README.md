# Documentación de Moonmake

Moonmake es un sistema de construcción ligero diseñado para proyectos C++, inspirado por makefile, con un enfoque en la simplicidad y facilidad de uso. Proporciona una interfaz basada en Python para gestionar dependencias, compilar código y manejar la construcción de proyectos.

## Conceptos Básicos

### Estructura del Proyecto
Un proyecto típico de moonmake sigue esta estructura:
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

El sistema Builder es el núcleo de moonmake. Gestiona el proceso de compilación a través de un conjunto de reglas que definen cómo se deben construir los archivos y sus dependencias.

Características principales:
- Seguimiento automático de dependencias
- Construcciones incrementales
- Soporte para bibliotecas estáticas
- Compatibilidad multiplataforma

#### Uso Básico del Builder

```python
builder = mmake.Builder()

# Regla para compilar un objetivo
builder.watch(
    archivos_objetivo,    # Archivos a construir
    dependencias,         # Dependencias requeridas
    comando_compilacion,  # Comando a ejecutar
    dependencias_extra    # Dependencias adicionales a vigilar
)
```

### Comandos Comunes

1. **Crear un Nuevo Proyecto**
```bash
python -m moonmake.create -n nombre_proyecto
```

2. **Instalar Dependencias**
```bash
python build.py install
```

3. **Construir el Proyecto**
```bash
python build.py
```

### Configuración de Construcción

El archivo `build.py` es donde configuras tu proyecto. Aquí un ejemplo básico:

```python
def execute():
    # Configurar rutas y banderas
    rutas_include = [...]
    rutas_lib = [...]
    
    # Configurar banderas del compilador
    BANDERAS_COMPILADOR = "-Wall -Wextra -std=c++2b"
    
    # Crear builder
    builder = mmake.Builder()
    
    # Agregar reglas de construcción
    builder.watch(archivos_objetivo, dependencias, comando_compilacion)
    
    # Ejecutar construcción
    builder.compile_all()
```

### Gestión de Dependencias

Moonmake incluye un sistema simple de gestión de dependencias:

```python
def install():
    mmake.download_dependency(
        url,           # URL de la dependencia
        nombre,        # Nombre de la dependencia
        dir_destino,   # Directorio de instalación
        headers=["include"]  # Directorios de cabecera a copiar
    )
```

### Variables Especiales en Comandos

Al escribir comandos de construcción, puedes usar estas variables especiales:
- `$@` : El archivo objetivo
- `$<` : Dependencia del indice del archivo objetivo
- `$^` : Todas las dependencias
- `$?` : Dependencias extra

## Mejores Prácticas

1. **Organización del Proyecto**
   - Mantén los archivos de cabecera en `src/include`
   - Coloca el código de biblioteca en `src/lib`
   - Pon los ejecutables principales en `src/target`



2. **Dependencias**
   - Usa la función `install()` para gestionar dependencias externas
   - Mantén las versiones de dependencias sincronizadas usando el sistema de enlaces

3. **Reglas de Construcción**
   - Usa las banderas de compilador apropiadas para tu proyecto
   - Incluye las bibliotecas del sistema necesarias (ej. `-lgdi32` para Windows)
   - Vigila los cambios en los archivos de cabecera

## Soporte de Plataformas

Moonmake soporta:
- Windows (MinGW-w64)
- Linux
- macOS

Cada plataforma tiene configuraciones específicas manejadas automáticamente por el sistema de construcción.

## Referencia de Funciones Básicas

Esta sección explica las funciones básicas proporcionadas por moonmake que comúnmente usarás en tu archivo `build.py`.

### Funciones de Directorio y Rutas

#### `mmake.get_dir(__file__)`
```python
dir_path = mmake.get_dir(__file__)
```
Retorna la ruta relativa del directorio actual desde la raíz del espacio de trabajo. Útil para crear rutas relativas a tu script de construcción.

#### `mmake.get_extension()`
```python
EXTENSION = mmake.get_extension()
```
Retorna la extensión de ejecutable apropiada para la plataforma actual:
- Windows: `.exe`
- Linux: `""` (sin extensión)
- macOS: `""` (sin extensión)

### Descubrimiento y Gestión de Archivos

#### `mmake.discover(directory, endswith)`
```python
headers = mmake.discover(join(dir_path, "src", "include"), ".h++")
```
Encuentra recursivamente todos los archivos en un directorio que terminan con una extensión específica. Retorna una lista de rutas relativas.

Ejemplo:
```python
# Encontrar todos los archivos .cpp en src/lib
cpp_files = mmake.discover("src/lib", ".cpp")
# Resultado: ["main.cpp", "utils/helper.cpp", ...]
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
Cambia la extensión de una lista de archivos y opcionalmente los mueve a un nuevo directorio. Útil para generar rutas de archivos objeto a partir de archivos fuente.

### Gestión de Dependencias

#### `mmake.download_dependency(url, name, target_dir, headers=["include"])`
```python
mmake.download_dependency(
    "https://example.com/lib.zip",
    "mylib",
    ".moonmake/dependencies",
    headers=["include"]
)
```
Descarga e instala una dependencia externa. Realiza:
- Descarga la dependencia desde la URL
- La extrae al directorio destino
- Copia los archivos de cabecera desde los directorios especificados
- Gestiona el seguimiento de versiones a través de un archivo de enlace

### Utilidades de Rutas y Banderas

#### `mmake.join_with_flag(paths, flag)`
```python
INCLUDE_FLAGS = mmake.join_with_flag(include_paths, "-I")
# Resultado: "-I/ruta1 -I/ruta2 -I/ruta3"
```
Une una lista de rutas con una bandera específica. Comúnmente usado para generar banderas del compilador como `-I` para includes o `-L` para rutas de bibliotecas.

#### `mmake.strip_lib_prefix(name)`
```python
lib_name = mmake.strip_lib_prefix("libraylib.a")
# Resultado: "raylib.a"
```
Elimina el prefijo "lib" de los nombres de bibliotecas. Útil al generar banderas del enlazador.

### Funciones del Sistema de Construcción

#### `mmake.Builder()`
```python
builder = mmake.Builder()
```
Crea una nueva instancia del sistema de construcción. Esta es la clase principal que usarás para definir reglas de construcción.

#### `builder.watch(target, dependencies, command, extra_dependencies=[])`
```python
builder.watch(
    archivos_objetivo,     # Archivos a construir
    archivos_dependencia,  # Dependencias requeridas
    "g++ $< -o $@",       # Comando de construcción
    dependencias_extra     # Archivos adicionales a vigilar
)
```
Define una regla de construcción. El comando puede usar variables especiales:
- `$@`: Archivo objetivo
- `$<`: Primera dependencia
- `$^`: Todas las dependencias
- `$?`: Dependencias extra

#### `builder.compile_all()`
```python
builder.compile_all()
```
Ejecuta todas las reglas de construcción en el orden correcto, respetando las dependencias.

### Interfaz de Línea de Comandos

#### `mmake.arguments_cmd(sys.argv, execute, install)`
```python
if __name__ == "__main__":
    mmake.arguments_cmd(sys.argv, execute, install)
```
Maneja los argumentos de línea de comandos para tu script de construcción. Soporta:
- `python build.py`: Ejecuta la función `execute()`
- `python build.py install`: Ejecuta la función `install()`

### Ejemplo de Uso

Aquí hay un ejemplo completo que muestra cómo estas funciones trabajan juntas:

```python
import moonmake as mmake
from os.path import join
import platform
import sys

dir_path = mmake.get_dir(__file__)

def install():
    # Descargar e instalar raylib
    raylib_url = "https://github.com/raysan5/raylib/releases/download/5.5/raylib-5.5_win64_mingw-w64.zip"
    mmake.download_dependency(
        raylib_url,
        "raylib",
        ".moonmake/dependencies",
        headers=["include"]
    )

def execute():
    # Encontrar todos los archivos fuente
    cpp_files = mmake.discover(join(dir_path, "src"), ".cpp")
    
    # Generar rutas de archivos objeto
    obj_files = mmake.change_extension(
        cpp_files,
        join(dir_path, ".moonmake", "obj"),
        old=".cpp",
        new=".o"
    )
    
    # Configurar rutas de inclusión
    include_paths = [
        join(".moonmake", "dependencies", "headers"),
        join(dir_path, "src", "include")
    ]
    INCLUDE_FLAGS = mmake.join_with_flag(include_paths, "-I")
    
    # Crear y configurar builder
    builder = mmake.Builder()
    
    # Agregar reglas de construcción
    builder.watch(
        obj_files,
        cpp_files,
        f"g++ -c $< -o $@ -Wall -Wextra {INCLUDE_FLAGS}"
    )
    
    # Ejecutar construcción
    builder.compile_all()

if __name__ == "__main__":
    mmake.arguments_cmd(sys.argv, execute, install) 


```

> i love math :)