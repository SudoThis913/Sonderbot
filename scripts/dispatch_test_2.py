from pathlib import Path
import os
import sys
import inspect
import pkgutil
from importlib import import_module
from Apps.sonderbotapp import SonderbotApp

def dynamic_import():
    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        imported_module = import_module(name, package='Apps')

        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            print(i)
            if inspect.isclass(attribute) and issubclass(attribute, SonderbotApp):
                setattr(sys.modules[__name__], name, attribute)
                print(name)

def dynamic_import2():
    currentdir = Path(__file__).parent
    print (currentdir)
    for r,d,f in os.walk(currentdir):

if __name__ == '__main__':
    dynamic_import2()