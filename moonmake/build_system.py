from pathlib import Path
from os.path import join,getmtime,dirname,abspath,isdir
import os.path as pathutils
from os import makedirs,getcwd,sep,listdir
from re import match
import zipfile
import shutil
import requests
import subprocess
def download_zip(url:str,output_dir:str,name:str):
    body=requests.get(url)
    zip_dir=join(output_dir,"zips")
    zip_path=join(zip_dir,f"{name}.zip")
    makedirs(zip_dir,exist_ok=True)
    with open(zip_path,"wb") as outfile:
        outfile.write(body.content)

    source_path=join(output_dir,"source",name)
    makedirs(source_path,exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(source_path)
def copy_all_to(source_path:str,destiny_dir:str):
    how_many=0
    maybe_dir=source_path
    for f in listdir(source_path):
        if not isdir(join(source_path,f)):
            break
        how_many+=1
        maybe_dir=join(f)
    target=source_path
    if how_many!=0:
        target=join(source_path,maybe_dir)
    shutil.copytree(target,destiny_dir)
def delete_dir(source_path:str):
    shutil.rmtree(source_path)

"""
the url is the url of the zip
the target dir is where the dependency will be installed, i will be installing this in lib,source, zip, headers
the argument headers is by default ["."], its defined like that in case you want to do some weird shit
static_lib is where the files .a are installed
the dll i havent added that yet so dont use it

"""
def generate_key(url:str,command:str,headers:list[str],static_lib:str,dlls:list[str]):
    return f"{command}-{url}-{".".join(headers)}-{static_lib}-{".".join(dlls)}"
def download_dependency(url:str,name:str,target_dir:str,command:str="",headers=["."],static_lib=["."],dlls=[]):
    linkdir=join(target_dir,"links")
    makedirs(linkdir,exist_ok=True)
    link_path=join(linkdir,name)
    open(link_path,"a").close()
    with open(link_path,"r+") as linkfile:
        link_url=linkfile.read()
        k=generate_key(url,command,headers,"-".join(static_lib),dlls)
        if link_url==k: return 
        try:
            delete_dir(join(target_dir,"headers",name))
            print(f"[REPLACING] : {name}")
        except:
            pass
        linkfile.seek(0)
        linkfile.write(k)
        linkfile.truncate()
    print(f"[DOWNLOADING] : {name}")
    download_zip(url,target_dir,name)
    source_files=join(target_dir,"source",name)    
    if command is not "":
        execute_command(command,cwd=source_files)
    if len(dlls)>0:
        print("TODO: add support to dll finding :)")        
    static_libs=[join (target_dir,"source",name,f) for f in discover(source_files,".a")]
    static_libs_names=[pathutils.split(i)[-1] for i in static_libs ]
    for (i,f) in enumerate(static_libs):
        d=join(target_dir,"lib",static_libs_names[i])
        makedirs(dirname(d),exist_ok=True)


        shutil.copy(f,d)
    for header in headers:
        copy_all_to(join(source_files,header),join(target_dir,"headers",name))
        
    

def get_dir(p:str):
    cwd=getcwd()
    raw_dir= dirname(abspath(p))
    return join(".",*raw_dir.split(sep)[len(cwd.split(sep)):])
    
# $^-> all $< each of the dependencies $@ this one $?
# we get the date of the file, just for checking if there is any new version
def get_date_file(path:str)->float:
    try: return getmtime(path)
    except: return -1
# then we need to verify if something contains this
def execute_command(command:str,show_command=True,cwd="."):
    command=command.replace("\\","/")
    if command is "":return 
    f=lambda x: x
    if show_command:
        print(command)
        f=lambda x: print(x)    
    result=subprocess.run(command,capture_output=True, text=True,shell=True,cwd=cwd)
    if result.stderr is not "":
        f(result.stderr)
        exit()
    if result.stdout is not "":
        f(result.stdout)
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
    file_list: list[str] = list([
        path.relative_to(base_path).as_posix() 
        for path in base_path.rglob(f"*{endswith}")])
    return file_list
"""
this is a simple function used for adding a new dependency or list of dependencies into a queue of compiling
you need to pass the command for compiling it.
the files that you will be building
and the files that it requires.
extra_dependencies are just in case you dont want to check anything and you just want to pass everything into it
"""



""" what this is for? well its for keeping some kind of order when compiling  our files
 it doesnt need much, and its just a simple tool for managing the scripting part for our dependencies yk
 you can also configure everything you want here if you are bored or anything
"""
class Build():
    
    def __init__(self,build:list[str],dependencies:list[str],command: str,extra_dependencies:list[str]=[],show_command=True):
        self.build:list[str]=build
        self.dependencies:list[str]=dependencies
        self.extra_dependencies:list[str]=extra_dependencies
        self.command:str=command
        self.show_command=show_command

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
    def compile_all(self,file:str,builder)->bool:
        build_file_date=get_date_file(file)
        recompile=build_file_date==-1        
        for (i,d) in enumerate(self.dependencies):
            dependency_date=get_date_file(d)
            if build_file_date < dependency_date or dependency_date==-1: 
                builder.call_dependency(self.dependencies)
                recompile=True
                break
        return recompile
    # $<
    def compile_each(self,file:str,dependency:str,builder)->bool:
        build_file_date=get_date_file(file)
        dependency_date=get_date_file(dependency)
        recompile=build_file_date==-1
        if build_file_date<dependency_date or dependency_date==-1:
            builder.call_dependency(self.dependencies)
            recompile=True
        return recompile
      
    def compile(self,builder)->int:
        total_compiled=0
        for (i,bf) in enumerate(self.build):
            build_command=self.command.replace("$@",bf).replace("$?"," ".join(self.extra_dependencies))
            recompile=self.check_on_extra(bf)
            if "$^" in build_command: #all dependencies will be passed into our file
                build_command=build_command.replace("$^"," ".join(self.dependencies))
                recompile|=self.compile_all(bf,builder)
            if "$<" in build_command :# we need pass the argument of each index
                build_command=build_command.replace("$<",self.dependencies[i])
                recompile|=self.compile_each(bf,self.dependencies[i],builder)                
            if not recompile: continue
            total_compiled+=1
            d=dirname(bf)
            if d is not "":
                makedirs(d,exist_ok=True)
            
            execute_command(build_command,show_command=self.show_command)     
        return total_compiled 
#something for internal usage
class Builder:
    def __init__(self):
        self.queue_builds=[]
    def call_dependency(self,dependencies:list[str]):
        b=next((b for b in self.queue_builds if b.build==dependencies),None)
        if b==None:
            return
        b.compile(self)
    def watch(self,build:list[str],need:list[str],command:str,extra_dependencies:list[str]=[],show_command=True):
        build_list=build
        self.queue_builds.append(Build(build,need,command,extra_dependencies=extra_dependencies,show_command=True))
    def compile_all(self):
        total_compiled=sum([b.compile(self) for b in reversed(self.queue_builds)])
        if total_compiled is 0:
            print("Everything seems to be on date")


