from pathlib import Path
from pathlib import PurePath
import os
import sys
import inspect
import pkgutil
from importlib import import_module
from importlib import util as il
from Apps.sonderbotapp import SonderbotApp

def dynamic_import():
    # Dynamically imports Sonderbot App modules.
    # Imports SBA apps, saves them in an array and returns them to the Sonderbot
    # Compiles a dispatch table of commands from each app and returns it to the Sonderbot.
    # TODO: Subdirectory package importing (currently all SBA apps must be on same level)

    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        print(__name__)
        print(name)
        print(os.path.basename(__file__))
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
                has_dynamic_import = getattr(attribute, "dynamic_import", None)
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
    for (pre, name, sub) in pkgutil.iter_modules([Path(__file__).parent]):
        #print(__name__)
        print(name)
        print(sub)
        print(pre )
        if "sba_" in name:
            print(name)
            imported_mod = import_module(name, Path(__file__).parent)
            x = imported_mod.loader()
            print(str(x.get_dispatch()))
        #print(os.path.basename(__file__))


# THIS ONE WORKS THE WAY I WANT IT TO YAY!
def dynamic_import3():
    for r, d, f in os.walk(Path(__file__).parent):
        for file in f:
            if "sba_" in file and file.endswith(".py"):
                print(file, r)
                spec = il.spec_from_file_location(file, str(os.path.join(r,file)))
                print(spec)
                foo = il.module_from_spec(spec)
                spec.loader.exec_module(foo)
                try:
                    foo.loader()
                except Exception as e:
                    print("Failed to load")
                    print(e)
if __name__ == '__main__':
    dynamic_import3()
