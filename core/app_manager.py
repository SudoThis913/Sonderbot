# core/app_manager.py

import importlib
from typing import Dict, List, Type
from core.models import Message
from core.logger import setup_logger
from core.sonderbot_app import SonderbotApp

logger = setup_logger("app")

class AppManager:
    def __init__(self):
        self.active_apps: Dict[str, List[SonderbotApp]] = {}
        self.registry: Dict[str, Type[SonderbotApp]] = {}

    def _make_key(self, host_id: str, channel: str) -> str:
        return f"{host_id}:{channel}"

    def register_app(self, app_cls: Type[SonderbotApp]):
        name = app_cls.friendly_name()
        if name in self.registry:
            logger.warning(f"App '{name}' already registered. Overwriting.")
        self.registry[name] = app_cls
        logger.info(f"Registered app '{name}' -> {app_cls.__module__}.{app_cls.__name__}")

    async def load_apps(self, host_id: str, channel: str, app_names: List[str]):
        key = self._make_key(host_id, channel)
        self.active_apps[key] = []

        for name in app_names:
            cls = self.registry.get(name)
            if not cls:
                try:
                    module = importlib.import_module(f"apps.{name}.{name}")
                    for attr in dir(module):
                        obj = getattr(module, attr)
                        if isinstance(obj, type) and issubclass(obj, SonderbotApp) and obj.friendly_name() == name:
                            cls = obj
                            self.register_app(cls)
                            break
                except Exception as e:
                    logger.error(f"Failed to import app '{name}': {e}")
                    continue

            if cls:
                instance = cls(channel=channel, host_id=host_id)
                await instance.setup()
                self.active_apps[key].append(instance)
                logger.info(f"Loaded app '{name}' for {host_id}#{channel}")

    async def unload_all(self):
        for app_list in self.active_apps.values():
            for app in app_list:
                await app.teardown()
        self.active_apps.clear()

    async def dispatch_message(self, message: Message):
        key = self._make_key(message.host_id, message.channel)
        for app in self.active_apps.get(key, []):
            await app.handle(message)

    async def tick_all(self):
        for app_list in self.active_apps.values():
            for app in app_list:
                await app.on_tick()

    def list_apps(self):
        print("Active apps by channel:")
        for key, app_list in self.active_apps.items():
            app_names = [type(app).friendly_name() for app in app_list]
            print(f"  {key}: {', '.join(app_names)}")
