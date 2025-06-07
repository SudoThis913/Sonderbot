import asyncio
from core.config import load_config
from core.session_queues import SessionQueues
from protocols.irc import IRCConnection


async def test_irc_connection():
    # Load connection config from file or interactive prompt
    configs = load_config()
    queues = SessionQueues()

    tasks = []

    for config in configs:
        if config.is_irc():
            queue = queues.get(config.host_id)
            connection = IRCConnection(config, queue)
            tasks.append(connection.connect())

    # Run all connection tasks concurrently
    if tasks:
        await asyncio.gather(*tasks)
    else:
        print("No IRC connections defined in config.")


if __name__ == "__main__":
    try:
        asyncio.run(test_irc_connection())
    except KeyboardInterrupt:
        print("Test interrupted.")