from os import getcwd
from os.path import dirname,abspath
cwd=getcwd()
raw_dir= dirname(abspath(__file__))
print(raw_dir,cwd)