import moonmake as mmake
import sys
print(sys.argv)

def install():
    zip_url="https://www.sqlite.org/2025/sqlite-amalgamation-3490100.zip"
    mmake.download_dependency(zip_url,"sqlite",".moonmake/dependencies")
def execute():
    print("hello :)")
def arguments_cmd(args:list[str],exe,inst):
    if len(args)>1 and args[1]=="install":
        inst()
        return
    exe()

if __name__=="__main__":
    arguments_cmd(sys.argv,execute,install)


