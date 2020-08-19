import os
from pathlib import Path
from importlib import util as ium

class AppManager():
    pass


def import_sba():
    appsList = []
    sbaApps = {}

    # for root, directory, file
    for r, d, f in os.walk(Path(__file__).parent):
        for file in f:
            #If file is a Sonderbot Application file, make spec, import, load:
            if "sba_" in file and file.endswith(".py"):
                spec = ium.spec_from_file_location(file, str(os.path.join(r, file)))
                newapp = ium.module_from_spec(spec)
                spec.loader.exec_module(newapp)
                try:
                    #Loader is a function in sonderbot apps which returns the app as a class.
                    newappClass = newapp.loader()
                    appname = newappClass.appName
                    if appname not in sbaApps.keys():
                        dispatch = newappClass.returnDispatch()
                        sbaApps[appname] = newappClass

                except Exception as e:
                    print("Failed to load")
                    print(e)

if __name__ == '__main__':
    import_sba()