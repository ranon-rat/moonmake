# MoonMake

A simple package manager and build system for c++ and c projects.

Its simple, it doesnt requires that many things, and its as easy to install as this

"bash
git install github.com/ranon-rat/MoonMake
cd MoonMake
pip3 install .
"

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
