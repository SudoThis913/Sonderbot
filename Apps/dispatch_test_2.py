from pathlib import Path
from pathlib import PurePath
import os
import sys
import inspect
import pkgutil
from importlib import import_module
from Apps.sonderbotapp import SonderbotApp

def dynamic_import():
    # Dynamically imports Sonderbot App modules.
    # Imports SBA apps, saves them in an array and returns them to the Sonderbot
    # Compiles a dispatch table of commands from each app and returns it to the Sonderbot.
    # TODO: Subdirectory package importing (currently all SBA apps must be on same level)

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
    pass
if __name__ == '__main__':
    dynamic_import()
