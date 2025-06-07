# cli.py

import asyncio
import shlex
from core.session_manager import SessionManager
from core.secrets import set_secret, delete_secret

class SonderbotCLI:
    def __init__(self, session_manager: SessionManager):
        self.session = session_manager
        self.running = True

    async def run(self):
        print("Sonderbot CLI ready. Type 'help' for commands.")
        while self.running:
            try:
                raw = input("> ")
                args = shlex.split(raw)
                if not args:
                    continue
                cmd = args[0]
                await self.handle_command(cmd, args[1:])
            except (EOFError, KeyboardInterrupt):
                await self.shutdown()

    async def handle_command(self, cmd, args):
        match cmd:
            case "shutdown" | "exit":
                await self.shutdown()
            case "reload-config":
                print("Reloading config...")
                await self.session.shutdown()
                await self.session.start_all()
            case "reload-apps":
                print("Reloading applications...")
                await self.session.reload_apps()
            case "send":
                if len(args) < 3:
                    print("Usage: send <host_id> <channel> <message>")
                else:
                    host, channel = args[0], args[1]
                    message = " ".join(args[2:])
                    await self.session.send_direct(host, channel, message)
            case "apps":
                self.session.app_manager.list_apps()
            case "set-secret":
                if len(args) != 1:
                    print("Usage: set-secret <service_key>")
                else:
                    set_secret(args[0])
            case "delete-secret":
                if len(args) != 1:
                    print("Usage: delete-secret <service_key>")
                else:
                    delete_secret(args[0])
            case "log":
                print("Not implemented yet: log viewer")
            case "help":
                self.print_help()
            case _:
                print(f"Unknown command: {cmd}")

    def print_help(self):
        print("""
Commands:
  shutdown / exit             Quit Sonderbot
  reload-config               Reload config.json and restart connections
  reload-apps                 Reload only apps without reconnecting
  send <host> <chan> <msg>    Send raw message
  apps                        List active apps by channel
  log <host> <chan>           Show recent messages (TODO)
  set-secret <key>            Store a password in keyring
  delete-secret <key>         Remove a stored password
  help                        Show this message
        """)

    async def shutdown(self):
        print("Shutting down...")
        self.running = False
        await self.session.shutdown()
        exit(0)
