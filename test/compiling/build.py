import re
from os.path import getmtime

"""
what i am going to do?

well thats its completely simple, what i am going to do is parse the 
dfile that was generated into 
"""
def get_date_file(path:str):
    try: return getmtime(path)
    except: return -1
analyze_file="main.c++"
pattern=re.compile(r'^[\w\/.\-+]+:\n',re.MULTILINE)

with open(analyze_file.replace(".c++",".d")) as f:
    text = f.read()

matches = list(map( lambda l: l[:-2], pattern.findall(text)))
base_file_date=get_date_file(analyze_file)
for file in matches:
    file_date= get_date_file(file)
    if file_date> base_file_date or file_date==-1:
        print(f"wtf the file {file} is more recent than the one that we have we should compile")

print(matches)
    