import platform
from os.path import join, isdir,isfile
import requests
import zipfile
get_extension=lambda: {"Windows":".exe","Linux":"","Darwin":""}[ platform.system()]
# this is just for changing the extensions, its for pattern matching
def change_extension(files:list[str],new_path:str,old:str="",new:str=""):
    return list([join(new_path,f.replace(old,new)) for f in files]) 
# in case you want to add the installation of the dependencies part :)
def arguments_cmd(args:list[str],execute:(),install:()):
    if len(args)>1 and args[1]=="install":
        install()
        return
    execute()
does_exist=lambda route: isdir(route) or isfile(route)
clean_routes=lambda routes:filter(does_exist,routes)
def join_with_flag(routes:list[str],flag:str):
    complete=""
    for i in routes:
        print(i)
        complete+=f" {flag}{i}"
    return complete
    #return " ".join(map(lambda r:f"{flag}{r}",clean_routes(routes))) 


def strip_lib_prefix(name: str) -> str:
    if name.startswith("lib"):
        return name[3:]  # Quita los primeros 3 caracteres
    return name