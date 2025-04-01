# main.py

import asyncio
import platform
import signal
from core.session_manager import SessionManager

async def main():
    session = SessionManager()
    stop_event = asyncio.Event()

    async def shutdown():
        print("\nShutting down...")
        stop_event.set()

    if platform.system() != "Windows":
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))
    else:
        # On Windows, we rely on catching KeyboardInterrupt
        asyncio.create_task(session.start_all())

    try:
        if platform.system() != "Windows":
            await session.start_all()
        await stop_event.wait()
    except KeyboardInterrupt:
        await shutdown()
    finally:
        await session.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
