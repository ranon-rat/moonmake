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
join_with_flag=lambda routes,flag: " ".join(map(lambda r:f"{flag}{r}",clean_routes(routes)))  
