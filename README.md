# MoonMake

A simple package manager and build system for c++ and c projects.

Its simple, it doesnt requires that many things, and its as easy to install as this


```bash
git install github.com/ranon-rat/moonmake
cd moonmake
pip3 install .
```

## motivations for this

i just want to improve my understanding of the c/c++ compiler and I also want to start building bigger and more cool projects.

I hate makefile since it gives a lot limitations( and i dont want to touch ninja either ).

## sintax

```makefile
$^-> all 
$< each of the dependencies
$? extra dependencies 
$@ the building part
```

And this is how its supposed to look like in action:

```py
import moonmake as mmake
from os.path import join

dir_path =mmake.get_dir(__file__)
# Lista los archivos en el directorio
if __name__=="__main__":
    example_files=list([join("example",f) for f in (mmake.discover(join(dir_path,"example"),".cpp"))])
    example_obj=list([join(dir_path,"obj",f.replace(".cpp",".o")) for f in example_files])
    mmake.watch([join(dir_path,"main.exe")],example_obj,"g++ $^ -o $@")
    mmake.watch(example_obj,list([join(dir_path,i) for i in example_files]),"g++ -c $< -o $@")
    mmake.compile_all()
```

## TODO

- [x] build system
- [x] package manager
- [x] configure your own installation
