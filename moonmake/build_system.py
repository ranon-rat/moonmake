from pathlib import Path
from os.path import join,getmtime,dirname,abspath
from os import makedirs,getcwd,sep
from re import match
import subprocess

# $^-> all $< each of the dependencies $@ this one $?
queueBuilds=[]
# we get the date of the file, just for checking if there is any new version
def get_date_file(path:str)->float:
    try: return getmtime(path)
    except: return -1
# then we need to verify if something contains this
def execute_command(command:str,capture_output=True, text=True):

    if command is "":return 
    f=lambda x: x
    if capture_output:
        print(command)
        f=lambda x: print(x)    
    result=subprocess.run(command.split(" "),capture_output=capture_output, text=text)
    if result.stderr is not "":
        f(result.stderr)
        exit()
    if result.stdout is not "":
        f(result.stdout)

    

""" what this is for? well its for keeping some kind of order when compiling  our files
 it doesnt need much, and its just a simple tool for managing the scripting part for our dependencies yk
 you can also configure everything you want here if you are bored or anything
"""
class Build():
    
    def __init__(self,build:list[str],dependencies:list[str],command: str,extra_dependencies:list[str]=[],capture_output=True, text=True):
        self.build:list[str]=build
        self.dependencies:list[str]=dependencies
        self.extra_dependencies:list[str]=extra_dependencies
        self.command:str=command
        self.capture_output=capture_output
        self.text=text

    #$?
    def check_on_extra(self,file:str)->bool:
        build_file_date=get_date_file(file)
        recompile=build_file_date==-1      
        for (i,d) in enumerate(self.extra_dependencies):
            dependency_date=get_date_file(d)
            if dependency_date==-1:
               print(f"{d} doesnt exists")
               exit()
            if build_file_date<dependency_date or dependency_date==-1:
                recompile=True  
        return recompile
    # $^
    def compile_all(self,file:str)->bool:
        build_file_date=get_date_file(file)
        recompile=build_file_date==-1        
        for (i,d) in enumerate(self.dependencies):
            dependency_date=get_date_file(d)
            if build_file_date < dependency_date or dependency_date==-1: 
                call_dependency(self.dependencies)
                recompile=True
                break
        return recompile
    # $<
    def compile_each(self,file:str,dependency:str,index:int)->bool:
        build_file_date=get_date_file(file)
        dependency_date=get_date_file(dependency)
        recompile=build_file_date==-1
        if build_file_date<dependency_date or dependency_date==-1:
            call_dependency(dependency)
            recompile
        return recompile
      
    def compile(self)->int:
        total_compiled=0
        for (i,bf) in enumerate(self.build):
            build_command=self.command.replace("$@",bf).replace("$?"," ".join(self.extra_dependencies))
            recompile=self.check_on_extra(bf)
            if "$^" in build_command: #all dependencies will be passed into our file
                build_command=build_command.replace("$^"," ".join(self.dependencies))
                recompile|=self.compile_all(bf)
            if "$<" in build_command :# we need pass the argument of each index
                build_command=build_command.replace("$<",self.dependencies[i])
                recompile|=self.compile_each(bf,self.dependencies[i],i)                
            if not recompile: continue
            total_compiled+=1
            d=dirname(bf)
            if d is not "":
                makedirs(d,exist_ok=True)
            
            execute_command(build_command,capture_output=self.capture_output,text=self.text)     
        return total_compiled 
#something for internal usage
def call_dependency(dependencies:list[str]):
    global queueBuilds
    b=next((b for b in queueBuilds if b.build==dependencies),None)
    if b is None:
        return
    b.compile()
"""
this will return you a list of files that are in the directory that you specified
the ends with its important because with this you can filter the files that you want
it will return you the directions of the files 
but they will be cleared, so you if you are calling something from a directory that looks like this
src
 |-c.cpp
 |--a
   |-a.cpp
   |-b.cpp
you will receive something like this
a/a.cpp
a/b.cpp
c.cpp
bbut you will not receive src :D
"""
def discover(directory: str, endswith: str) -> list[str]:
    base_path = Path(directory).resolve()
    file_list: list[str] = []
    for path in base_path.rglob(f"*{endswith}"):
        file_list.append(path.relative_to(base_path).as_posix())  
    
    return file_list
"""
this is a simple function used for adding a new dependency or list of dependencies into a queue of compiling
you need to pass the command for compiling it.
the files that you will be building
and the files that it requires.
extra_dependencies are just in case you dont want to check anything and you just want to pass everything into it
"""
def watch(build:list[str],need:list[str],command:str,extra_dependencies:list[str]=[],capture_output=True, text=True):
    global queueBuilds
    build_list=build
  
    queueBuilds.append(Build(build,need,command,extra_dependencies=extra_dependencies,capture_output=True, text=True))
def get_dir(p:str):
    cwd=getcwd()
    raw_dir= dirname(abspath(p))
    return join(".",*raw_dir.split(sep)[len(cwd.split(sep)):])

def compile_all():
    global queueBuilds
    total_compiled=0
    for b in reversed(queueBuilds):
        total_compiled+=b.compile()
    if total_compiled is 0:
        print("Everything seems to be on date")