import platform
from os.path import join
get_extension=lambda: {"Windows":".exe","Linux":"","Darwin":""}[ platform.system()]
def change_extension(files:list[str],new_path:str,old:str="",new:str=""):
    return list([join(new_path,f.replace(old,new)) for f in files])