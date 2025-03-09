import moonmake as mmake

if __name__=="__main__":
    example_files=(mmake.discover("example/",".cpp"))
    example_obj=list(["obj/"+f.replace(".cpp",".o") for f in example_files])
    mmake.watch(example_obj,example_files,"g++ -c $< -o $@")
    mmake.watch(["main.exe"],example_obj,"g++ $^ -o $@")
    mmake.compile_all()
