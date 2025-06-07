# core/app_manager.py

import importlib
import sys
from pathlib import Path
from typing import Dict, List, Type
from core.models import Message
from core.logger import setup_logger
from core.sonderbot_app import SonderbotApp
import asyncio

logger = setup_logger("apps")

class AppManager:
    def __init__(self):
        self.active_apps: Dict[str, List[SonderbotApp]] = {}
        self.registry: Dict[str, Type[SonderbotApp]] = {}

        # Ensure apps/ is importable
        apps_path = Path(__file__).resolve().parent.parent / "apps"
        if str(apps_path) not in sys.path:
            sys.path.insert(0, str(apps_path))

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

        for friendly_name in app_names:
            logger.info(f"Attempting to load app: '{friendly_name}' for {host_id}#{channel}")
            cls = self.registry.get(friendly_name)

            if not cls:
                logger.debug(f"App '{friendly_name}' not found in registry. Attempting dynamic import.")
                try:
                    from apps import __path__ as apps_path_list
                    logger.debug(f"App '{friendly_name}' not found in registry. Attempting dynamic import.")
                    for apps_path in apps_path_list:
                        for subdir in Path(apps_path).iterdir():
                            if subdir.is_dir():
                                module_file = subdir / f"{subdir.name}.py"
                                if module_file.exists():
                                    module_path = f"apps.{subdir.name}.{subdir.name}"
                                    try:
                                        logger.debug(f"Trying to import module '{module_path}'")
                                        module = importlib.import_module(module_path)
                                        for attr in dir(module):
                                            obj = getattr(module, attr)
                                            if (
                                                isinstance(obj, type)
                                                and issubclass(obj, SonderbotApp)
                                                and obj.friendly_name() == friendly_name
                                            ):
                                                cls = obj
                                                self.register_app(cls)
                                                logger.info(f"Discovered and registered app '{friendly_name}' from '{module_path}'")
                                                break
                                        if cls:
                                            break
                                    except Exception as inner_e:
                                        logger.debug(f"Failed to import '{module_path}': {inner_e}", exc_info=True)
                        if cls:
                            break

                except Exception as e:
                    logger.error(f"Failed during dynamic discovery for app '{friendly_name}': {e}", exc_info=True)
                    continue

            if cls:
                try:
                    instance = cls(channel=channel, host_id=host_id)
                    await instance.setup()
                    self.active_apps[key].append(instance)
                    logger.info(f"Loaded app '{friendly_name}' for {host_id}#{channel}")
                except Exception as inst_e:
                    logger.error(f"Failed to initialize app '{friendly_name}': {inst_e}", exc_info=True)
            else:
                logger.error(f"Unable to load app '{friendly_name}' for {host_id}#{channel}. App not found or failed to import.")

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


# CLI input loop that does not block asyncio event loop
async def cli_input_loop(session_manager, stop_event: asyncio.Event):
    while not stop_event.is_set():
        try:
            cmd = await asyncio.to_thread(input, "Sonderbot > ")
            cmd = cmd.strip().lower()

            if cmd == "apps":
                session_manager.app_manager.list_apps()
            elif cmd == "quit":
                stop_event.set()
            else:
                print("Unknown command.")
        except (EOFError, KeyboardInterrupt):
            stop_event.set()
