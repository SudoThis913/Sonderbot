from pathlib import Path
from pathlib import PurePath
import os
import sys
import inspect
import pkgutil
from importlib import import_module
from Apps.sonderbotapp import SonderbotApp

def dynamic_import():


    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        #print(__name__)
        #print(os.path.basename(__file__))
        imported_module = import_module(name, package='Apps')
        #print(imported_module)
        for i in dir(imported_module):
            #print(i)
            attribute = getattr(imported_module, i)
            #print(i)
            if inspect.isclass(attribute) and issubclass(attribute, SonderbotApp):
                setattr(sys.modules[__name__], name, attribute)
                print(name)
                #print(attribute)
                has_get_dispatch = getattr(attribute, "get_dispatch", None)
                has_dynamic_import = getattr(attribute,"dynamic_import", None)
                if callable(has_get_dispatch):
                    if callable(has_dynamic_import):
                        pass
                    else:
                        print("X")
                        try:
                            x = imported_module.loader()
                            print(str(x.get_dispatch()))
                        except Exception as e:
                            print(e)

def dynamic_import2():
    currentdir = Path(__file__).parent
    # Root, Directory, File
    for r,d,f in os.walk(currentdir):
        for item in f:
            print(item)
            if "sba_" in item and ".py" in item and ".pyc" not in item:
                print(r)
                x = os.path.basename(r)
                print(r)

                for (_, name, _) in pkgutil.iter_modules(r):
                    imported_module = import_module(name, package='Apps')
                    for i in dir(imported_module):
                        attribute = getattr(imported_module, i)
                        print(i)
                        if inspect.isclass(attribute) and issubclass(attribute, SonderbotApp):
                            setattr(sys.modules[__name__], name, attribute)
                            print(name)



if __name__ == '__main__':
    dynamic_import()