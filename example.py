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