"""import importlib.util
import sys
import inspect
import os
import pathlib
from Apps.sonderbotapp import *

# testing absolute file path importing and reloading

def main():
    currentdir = os.path.dirname(os.path.realpath(__file__))
    # app_path = os.path.join(currentdir, "Apps")
    files = []
    apps = []
    #root, directory, files
    for r, d, f in os.walk(currentdir): # replace with app_path if in top-level
        for item in f:
            if 'sba_' in item and ".pyc" not in item:
                #print("F:" + item)
                fp = os.path.join(r, item)
                ap = pathlib.PurePath(fp)
                ap = ap.parent.name
                files.append({"fp": os.path.join(r, item), "ap": ap, "sba": item})

    for item in files:
        newapp = importlib.import_module("Apps."+item["ap"]+"."+item["sba"])
        #newapp = importlib.import_module()
        x = newapp.sba_countfucks.main1()
        #newapp = importlib.import_module(item["fp"])

        for i in dir(newapp):
            attribute = getattr(newapp, i)
            #print(i)
            if inspect.isclass(attribute) and issubclass(attribute, SonderbotApp):
                print("X")
                setattr(sys.modules[__name__], item["sba"], attribute)
                print(attribute)
        #print(newapp)
        #module = getattr(newapp, 'main1')
        #x = module.main()

        #print(newapp)


        #for name, obj in inspect.getmembers(module, inspect.isclass):
         #   print(name)


        #spec = importlib.util.spec_from_file_location(item["sba"], item["fp"])
        #newmod = importlib.util.module_from_spec(spec)
        #spec.loader.exec_module(newmod)

        #for name, obj in inspect.getmembers(newapp):

    #if inspect.isclass(obj):
        #print("X")


pass

def main2():
    currentdir = os.path.dirname(os.path.realpath(__file__))
    # app_path = os.path.join(currentdir, "Apps")
    files = []
    apps = []
    #root, directory, files
    for r, d, f in os.walk(currentdir): # replace with app_path if in top-level
        for item in f:
            if 'sba_' in item:
                #print("F:" + item)
                fp = os.path.join(r, item)
                ap = pathlib.PurePath(fp)
                ap = ap.parent.name
                files.append({"fp": os.path.join(r, item), "ap": ap, "sba": item})







def import_from_apps(filepath):
    newApp = None
    expected_class = 'SonderbotApp'


if __name__ == '__main__':
    main()
"""