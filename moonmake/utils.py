import platform
from os.path import join, isdir,isfile
import requests
import zipfile
get_extension=lambda: {"Windows":".exe","Linux":"","Darwin":""}[ platform.system()]
def change_extension(files:list[str],new_path:str,old:str="",new:str=""):
    return list([join(new_path,f.replace(old,new)) for f in files]) 
def download_zip(url:str,output_path:str,name:str):
    body=requests.get(url)
    zip_path=join(output_path,"zips",f"{name}.zip")
    with open(zip_path,"w") as outfile:
        outfile.write(body.raw)
    source_path=join(output_path,"source")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(source_path)
  
does_exist=lambda route: isdir(route) or isfile(route)
clean_routes=lambda routes:filter(does_exist,routes)
join_with_flag=lambda routes,flag: " ".join(map(lambda r:f"{flag}{r}",clean_routes(routes)))  
