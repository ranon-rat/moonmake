import moonmake as mmake


if __name__=="__main__":
    example_files=(mmake.discover("example/",".cpp"))
    mmake.watch(["main.exe"],example_files,"g++ $^ -o $@")
    mmake.compile_all()

