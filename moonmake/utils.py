import platform
from os.path import join, isdir,isfile
get_extension=lambda: {"Windows":".exe","Linux":"","Darwin":""}[ platform.system()]
def change_extension(files:list[str],new_path:str,old:str="",new:str=""):
    return list([join(new_path,f.replace(old,new)) for f in files]) 
does_exist=lambda route: isdir(route) or isfile(route)
clean_routes=lambda routes:filter(does_exist,routes)
join_with_flag=lambda routes,flag: " ".join(map(lambda r:f"{flag}{r}",clean_routes(routes)))  
