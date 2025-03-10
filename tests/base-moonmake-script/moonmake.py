import moonmake as mmake
import platform
from os.path import join

dir_path =mmake.get_dir(__file__)
# Lista los archivos en el directorio
if __name__=="__main__":
    moonmake=".moonmake"
    
    CPP_VERSION="14"
    INCLUDE=f"-I{join(dir_path,"src","include")}  -I{join(".",moonmake,"dependencies","headers")} "
    FLAGS=f"-Wall -Wextra -std=c++${CPP_VERSION}"
    LINK=f"-L{join(".",dir_path,"moonmake","lib")} -L{join(".","moonmake","dependencies","lib")}"   

    extension=mmake.get_extension()
    main=mmake.Builder()

    target_files=list([f for f in  mmake.discover(join(dir_path,"src","target"),".cpp")])
    target_obj=mmake.change_extension(target_files,join(dir_path,moonmake,"obj","target"),old=".cpp",new=".o")
    target_bin=mmake.change_extension(target_files,join(dir_path,moonmake,"bin"),old=".cpp",new=extension)

    lib_files=list([f for f in  mmake.discover(join(dir_path,"src","lib"),".cpp")])
    lib_obj=mmake.change_extension(lib_files,join(dir_path,"obj","lib"),old=".cpp",new=".o")
    lib_static=join(dir_path,moonmake,"lib","libmoon.a")
    #so we generate the binaries
    main.watch(target_bin,target_obj,f"g++ $< -o $@ {FLAGS} {LINK}",extra_dependencies=[lib_static])
    #object files for the target_files :D
    main.watch(target_obj,target_files,f"g++ -c $< -o $@ {FLAGS} {INCLUDE} ")
    #we create a library for later linking it with our target binaries
    main.watch([lib_static],lib_obj,"ar rcs $@ $^")
    #we generate the object files of thebinaries
    main.watch(lib_obj,lib_files,f"g++ -c $< -o $@ {FLAGS} {INCLUDE}")

    main.compile_all()
