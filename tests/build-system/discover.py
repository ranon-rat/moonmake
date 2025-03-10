import moonmake as mmake
from os.path import join

dir_path =mmake.get_dir(__file__)
# Lista los archivos en el directorio
if __name__=="__main__":
    main=mmake.Builder()
    example_files=list([join("example",f) for f in (mmake.discover(join(dir_path,"example"),".cpp"))])
    example_obj=list([join(dir_path,"obj",f.replace(".cpp",".o")) for f in example_files])
    main.watch([join(dir_path,"main.exe")],example_obj,"g++ $^ -o $@")
    main.watch(example_obj,list([join(dir_path,i) for i in example_files]),"g++ -c $< -o $@")
    main.compile_all()
