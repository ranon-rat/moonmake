import moonmake as mmake
import platform
from os.path import join

dir_path =mmake.get_dir(__file__)
# Lista los archivos en el directorio
if __name__=="__main__":
    moonmake=".moonmake"
    
    CPP_VERSION="14"
    INCLUDE=f"-I{join(dir_path,"src","include")}  -I{join(".",moonmake,"dependencies","headers")} "
    mmake.discover()
    FLAGS=f"-Wall -Wextra -std=c++${CPP_VERSION}"
    LINK=f"-L{join(".",dir_path,moonmake,"lib")} -L{join(".",moonmake,"dependencies","lib")}"   

    extension=mmake.get_extension()
    main=mmake.Builder()
    static_a_files=mmake.Builder(join(".",moonmake,"dependencies","lib"),".a")
    dir_a_files=[join(".",moonmake,"dependencies","lib",a) for a in static_a_files]
    STATIC_LIBRARY=" ".join([f"-l{a.replace("lib","").replace(".a","")}" for a in static_a_files])

    target_files=list([f for f in  mmake.discover(join(dir_path,"src","target"),".cpp")])
    target_obj=mmake.change_extension(target_files,join(dir_path,moonmake,"obj","target"),old=".cpp",new=".o")
    target_bin=mmake.change_extension(target_files,join(dir_path,moonmake,"bin"),old=".cpp",new=extension)

    lib_files=list([f for f in  mmake.discover(join(dir_path,"src","lib"),".cpp")])
    lib_obj=mmake.change_extension(lib_files,join(dir_path,"obj","lib"),old=".cpp",new=".o")
    lib_static=join(dir_path,moonmake,"lib","libsrc.a")
    #so we generate the binaries
    main.watch(target_bin,target_obj,f"g++ $< -o $@ {FLAGS} {LINK} {STATIC_LIBRARY} -lsrc",extra_dependencies=[lib_static,*dir_a_files])
    #object files for the target_files :D
    main.watch(target_obj,target_files,f"g++ -c $< -o $@ {FLAGS} {INCLUDE} ")
    #we create a library for later linking it with our target binaries
    main.watch([lib_static],lib_obj,"ar rcs $@ $^")
    #we generate the object files of thebinaries
    main.watch(lib_obj,lib_files,f"g++ -c $< -o $@ {FLAGS} {INCLUDE}")

    main.compile_all()
