from os import makedirs
from os.path import join
import sys
import argparse

def build_folder(route:str):
    makedirs(route,exist_ok=True)

def create_new():

    moonmake_build=".moonmake"# its better to keep this thing hidden :)
    makedirs(join())
    print(sys.argv)

def main():
    parser=argparse.ArgumentParser(description="create a new moonmake project")
    subparsers = parser.add_subparsers(help="Avaible commands", dest="command")

    create_new()

if __name__=="__main__":
    main()