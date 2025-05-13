# Moonmake 🌙

[English](docs/en/README.md) | [Español](docs/es/README.md)

Moonmake is a lightweight, Python-based build system for C++ projects. It provides a simple and intuitive way to manage dependencies, compile code, and handle project builds across different platforms.
Inspired by makefile, made for my own purposes

## Features ✨

- 🚀 Simple and intuitive build system
- 📦 Easy dependency management
- 🔄 Incremental builds
- 📚 Static library support
- 🌍 Cross-platform (Windows, Linux, macOS)
- 🛠️ Flexible build configuration

## Quick Start 🚀

1. **Install Moonmake**
```bash
pip install moonmake
```

2. **Create a New Project**
```bash
python -m moonmake.create -n my_project
```

3. **Install Dependencies**
```bash
cd my_project
python build.py install
```

4. **Build Your Project**
```bash
python build.py
```

## Project Structure 📁

```
my_project/
├── .moonmake/          # Build system directory
│   ├── bin/           # Compiled binaries
│   ├── obj/           # Object files
│   ├── lib/           # Generated libraries
│   └── dependencies/  # External dependencies
├── src/
│   ├── include/       # Header files
│   ├── lib/           # Library source files
│   └── target/        # Main executable sources
└── build.py           # Build configuration
```

## Documentation 📚

For detailed documentation, please visit:
- [English Documentation](docs/en/README.md)
- [Documentación en Español](docs/es/README.md)

## Requirements 📋

- Python 3.6+
- C++ Compiler (g++/clang++)
- For Windows: MinGW-w64

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.


```bash
git install github.com/ranon-rat/moonmake
cd moonmake
pip3 install .
```