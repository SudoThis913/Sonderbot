#!/usr/bin/python3
import os
import asyncio
from pathlib import Path
from importlib import util as ium
from .sonderbotapp import sba_context, SonderbotApp

class AppManager():
    app_context = sba_context()
    appsList = []
    sbaApps = {}

    async def sba_loader(self):
        # for root, directory, file
        for r, d, f in os.walk(Path(__file__).parent):
            for file in f:
                #If file is a Sonderbot Application file, make spec, import, load:
                if "sba_" in file and file.endswith(".py"):
                    spec = ium.spec_from_file_location(file, str(os.path.join(r, file)))
                    newapp = ium.module_from_spec(spec)
                    spec.loader.exec_module(newapp)

    def sba_app_load(self, spec):
        newapp = ium.module_from_spec(spec)
        spec.loader.exec_module(newapp)
        try:
            # Loader is a function in sba apps which returns the app as a class.
            newappClass = newapp.loader()
            appname = newappClass.appName
            if appname not in self.sbaApps.keys():
                dispatch = newappClass.returnDispatch()
                self.sbaApps[appname] = newappClass
        except Exception as e:
            print("Failed to load")
            print(e)
if __name__ == '__main__':
    asyncio.run(AppManager().sba_loader())