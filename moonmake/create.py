from os import makedirs
from os.path import join
import sys
import argparse

BASE_MOONFILE="""#https://github.com/ranon-rat/moonmake
import moonmake as mmake
from os.path import join
import moonmake as mmake
from os.path import join
dir_path =mmake.get_dir(__file__)
# Lista los archivos en el directorio
if __name__=="__main__":
    moonmake_dir=".moonmake"
    CPP_VERSION="2b"
    INCLUDE=f"{mmake.join_with_flag([join(".",moonmake_dir,"dependencies","headers")],"-I")} -I{join(dir_path,"src","include")}"
    FLAGS=f"-Wall -Wextra -std=c++{CPP_VERSION}"
    LINK=f"{mmake.join_with_flag([join(moonmake_dir,"dependencies","lib")],"-L")} -L{join(dir_path,moonmake_dir,"lib")}"

    extension=mmake.get_extension()
    main=mmake.Builder()
    static_a_files=mmake.discover(join(".",moonmake_dir,"dependencies","lib"),".a")
    STATIC_LIBRARY=" ".join([f"-l{a.replace("lib","").replace(".a","")}" for a in static_a_files])
    headers=mmake.discover(join(dir_path,"src","include"),".h++")
    target_files=list([f for f in  mmake.discover(join(dir_path,"src","target"),".cpp")])
    target_obj=mmake.change_extension(target_files,join(dir_path,moonmake_dir,"obj","target"),old=".cpp",new=".o")
    target_bin=mmake.change_extension(target_files,join(dir_path,moonmake_dir,"bin"),old=".cpp",new=extension)

    lib_files=list([f for f in  mmake.discover(join(dir_path,"src","lib"),".cpp")])
    lib_obj=mmake.change_extension(lib_files,join(dir_path,moonmake_dir,"obj","lib"),old=".cpp",new=".o")
    lib_static=join(dir_path,moonmake_dir,"lib","libmsrc.a")
    #so we generate the binaries
    main.watch(list(map(lambda r:r,target_bin)),list(map(lambda r:r,target_obj)),f"g++  $< -o $@ {FLAGS} {LINK} {STATIC_LIBRARY} -lmsrc",extra_dependencies=[lib_static,*static_a_files])
    #object files for the target_files :D
    main.watch(target_obj,list(map(lambda r:join(".","src","target",r),target_files)),f"g++ -c $< -o $@ {FLAGS} {INCLUDE} ")
    #we create a library for later linking it with our target binaries
    main.watch([lib_static],lib_obj,"ar rcs $@ $^")
    #we generate the object files of thebinaries
    main.watch(lib_obj,list(map(lambda r:join(".","src","lib",r),lib_files)),f"g++ -c $< -o $@ {FLAGS} {INCLUDE}")

    main.compile_all()
"""
def build_folder(route:str,readme:str):
    makedirs(route,exist_ok=True)
    with open(join(route,"README.md"),"w") as f:
        f.write(readme+"\n")
def create_new(name:str):
    global BASE_MOONFILE
    moonmake=".moonmake"# its better to keep this thing hidden :)
    routes=[
        (join(".",name,moonmake,"obj"),"compiled object files"),#a,o,.exe
        (join(".",name,moonmake,"bin"),"binary files"),#a,o,.exe
        (join(".",name,moonmake,"lib"),"library files generated by the program"),#a,o,.exe
        (join(".",name,moonmake,"dependencies","headers"),"headers from the dependencies"),
        (join(".",name,moonmake,"dependencies","libs"),"libraries to link"),
        (join(".",name,"src","include"),"place here the header files and only initialize your functions"),
        (join(".",name,"src","target"),"here it goes the target files, every file that you place here will have its own binary"),
        (join(".",name,"src","lib"),"define your functions here"),
    ]
    for (p,r) in routes:build_folder(p,r)
    with open(join(".",name,"build.py"),"w") as f:
        f.write(BASE_MOONFILE)
def __main():
    parser=argparse.ArgumentParser(description="create a new moonmake project")
    parser.add_argument("-c","--compiler",help="select the compiler that you want to use",default="g++")
    parser.add_argument("-n","--name",help="the name of the project that you want to create",required=True)
    args=vars(parser.parse_args())
    name=args["name"]
    create_new(name)
if __name__=="__main__":
    __main()