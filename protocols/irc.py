import asyncio
import ssl
import traceback
from typing import Optional
from ssl import SSLCertVerificationError
from pathlib import Path

from core.models import ConnectionConfig, Message
from core.message_queue import MessageQueue
from core.logger import setup_logger
from core.certs import fetch_server_cert, make_ssl_context_with_local_cert
from core.config import dispatch_numeric_response, numeric_handler
from protocols.irc_error_codes import irc_errors as IRC_ERRORS
from core.db import DatabaseManager

logger = setup_logger("irc")


class IRCConnection:
    def __init__(self, config: ConnectionConfig, queue: MessageQueue):
        self.config = config
        self.queue = queue

        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None

        self.connected = False
        self.authenticated = False
        self.max_retries = 5
        self.reconnect_attempts = 0

        self.response_event = asyncio.Queue()

    async def connect(self):
        delay = 2
        while self.reconnect_attempts < self.max_retries:
            logger.info(f"[{self.config.hostname}] Connecting to IRC...")
            cert_path = Path(f"data/certs/{self.config.hostname}.pem")

            try:
                ssl_ctx = None
                if cert_path.exists():
                    logger.info(f"[{self.config.hostname}] Using cached certificate.")
                    ssl_ctx = make_ssl_context_with_local_cert(str(cert_path))
                elif self.config.use_ssl:
                    ssl_ctx = ssl.create_default_context()

                self.reader, self.writer = await asyncio.open_connection(
                    self.config.hostname, self.config.port, ssl=ssl_ctx
                )
                self.connected = True
                self.reconnect_attempts = 0

                listen_task = asyncio.create_task(self._listen_loop())
                send_task = asyncio.create_task(self._send_loop())
                await self._handshake_loop()
                try:
                    await asyncio.gather(listen_task, send_task)
                except asyncio.CancelledError:
                    logger.warning(f"[{self.config.hostname}] Connection tasks cancelled.")
                finally:
                    self.connected = False
                break

            except SSLCertVerificationError as ssl_err:
                print(f"SSL verification failed: {ssl_err}")
                if not cert_path.exists():
                    use_local = input(f"Trust and import certificate from {self.config.hostname}? [y/N]: ").strip().lower()
                    if use_local == 'y':
                        cert_path_str = fetch_server_cert(self.config.hostname, self.config.port)
                        print(f"✔ Certificate saved to {cert_path_str}")
                        ssl_ctx = make_ssl_context_with_local_cert(cert_path_str)
                        self.reader, self.writer = await asyncio.open_connection(
                            self.config.hostname, self.config.port, ssl=ssl_ctx
                        )
                        self.connected = True
                        self.reconnect_attempts = 0

                        listen_task = asyncio.create_task(self._listen_loop())
                        send_task = asyncio.create_task(self._send_loop())
                        await self._handshake_loop()
                        await asyncio.gather(listen_task, send_task)
                        return
                raise ssl_err

            except Exception as e:
                self.reconnect_attempts += 1
                logger.error(f"[{self.config.hostname}] Connection failed (attempt {self.reconnect_attempts}): {e}")
                traceback.print_exc()
                await asyncio.sleep(min(delay * (2 ** self.reconnect_attempts), 60))

    async def _handshake_loop(self):
        fallback_attempted = False
        while not self.authenticated and self.connected:
            await self._send_raw("CAP LS")
            await self._perform_handshake()
            try:
                response = await asyncio.wait_for(self.response_event.get(), timeout=20)
                if response == "001":
                    logger.info(f"[{self.config.hostname}] Successfully registered.")
                    self.authenticated = True

                    if self.config.chanserv_user and self.config.chanserv_pass:
                        auth_msg = f"IDENTIFY {self.config.chanserv_user} {self.config.chanserv_pass}"
                        await self.send_message("NickServ", auth_msg)
                        logger.info(f"[{self.config.hostname}] Sent IDENTIFY to NickServ")

                    if self.config.default_channel:
                        await self.join_channel(self.config.default_channel)

                    if self.config.extra_channels:
                        for chan in self.config.extra_channels:
                            await self.join_channel(chan)

                elif response == "433":
                    logger.warning(f"[{self.config.hostname}] Nickname already in use.")
                    if fallback_attempted:
                        logger.error(f"[{self.config.hostname}] All fallback nicknames exhausted.")
                        break
                    await self._cycle_nick()
                    fallback_attempted = True

            except asyncio.TimeoutError:
                logger.error(f"[{self.config.hostname}] Timed out waiting for welcome message (001).")
                break

    async def _perform_handshake(self):
        if self.config.botpass:
            await self._send_raw(f"PASS {self.config.botpass}")
        await self._send_raw(f"NICK {self.config.botnick}")
        await self._send_raw(f"USER {self.config.botnick} {self.config.hostname} {self.config.hostname} :Sonderbot")

    async def join_channel(self, channel: str):
        await self._send_raw(f"JOIN {channel}")

    async def send_message(self, channel: str, content: str):
        await self._send_raw(f"PRIVMSG {channel} :{content}")

    async def _send_loop(self):
        while self.connected:
            try:
                msg = await self.queue.get_outgoing()
                await self.send_message(msg.channel, msg.content)
            except Exception as e:
                logger.warning(f"Send loop error: {e}")

    async def _listen_loop(self):
        buffer = b""
        while self.connected:
            try:
                chunk = await self.reader.read(4096)
                if not chunk:
                    break

                buffer += chunk
                while b"\r\n" in buffer:
                    line, buffer = buffer.split(b"\r\n", 1)
                    decoded = line.decode(errors="ignore").strip()
                    logger.debug(f"[{self.config.hostname}] ← {decoded}")

                    if decoded.startswith("PING"):
                        payload = decoded.split(":", 1)[-1]
                        await self._send_raw(f"PONG :{payload}")

                    await self._handle_response(decoded)

            except Exception as e:
                logger.error(f"[{self.config.hostname}] Listener error: {e}")
                break

        self.connected = False

    async def _handle_response(self, response: str):
        if "NOTICE" in response:
            logger.debug(f"[{self.config.hostname}] NOTICE received: {response}")
        parts = response.split()
        if len(parts) >= 2 and parts[1].isdigit():
            await dispatch_numeric_response(self, parts)
            await self.response_event.put(parts[1])

        if "PRIVMSG" in response:
            parts = response.split(" ")
            user = response.split("!")[0][1:]
            channel = parts[2]
            content = " ".join(parts[3:])[1:]
            msg = Message(
                host_id=self.config.host_id,
                hostname=self.config.hostname,
                channel=channel,
                user=user,
                content=content,
            )
            await self.queue.put_incoming(msg)

    async def _cycle_nick(self):
        if self.config.botnick2 and self.config.botnick != self.config.botnick2:
            logger.info(f"[{self.config.hostname}] Switching to fallback nick.")
            self.config.botnick = self.config.botnick2
        elif self.config.botnick3 and self.config.botnick != self.config.botnick3:
            self.config.botnick = self.config.botnick3
        else:
            logger.error(f"[{self.config.hostname}] No available fallback nicknames.")

    async def _send_raw(self, data: str):
        if self.writer:
            logger.debug(f"[{self.config.hostname}] → {data}")
            self.writer.write((data + "\r\n").encode())
            await self.writer.drain()

    async def disconnect(self):
        if self.writer:
            try:
                await self._send_raw("QUIT :Sonderbot shutting down")
                self.writer.close()
                await self.writer.wait_closed()
            except ssl.SSLError as e:
                logger.warning(f"SSL error during shutdown: {e}")
            except Exception as e:
                logger.warning(f"Error during shutdown: {e}")
        self.connected = False


@numeric_handler(431)
async def handle_no_nick_given(connection, parts):
    logger.warning(f"[{connection.config.hostname}] Nickname not provided. Attempting fallback.")
    await connection._cycle_nick()
    await connection.disconnect()
    await connection.connect()


@numeric_handler(432)
async def handle_erroneous_nick(connection, parts):
    logger.warning(f"[{connection.config.hostname}] Erroneous nickname. Cycling...")
    await connection._cycle_nick()
    await connection.disconnect()
    await connection.connect()


@numeric_handler(464)
async def handle_password_mismatch(connection, parts):
    logger.error(f"[{connection.config.hostname}] Password mismatch. Shutting down connection.")
    await connection.disconnect()


@numeric_handler(474)
async def handle_banned_from_channel(connection, parts):
    if len(parts) > 3:
        channel = parts[3]
        logger.warning(f"[{connection.config.hostname}] Banned from {channel}. Skipping join.")


@numeric_handler(475)
async def handle_bad_channel_key(connection, parts):
    if len(parts) > 3:
        channel = parts[3]
        logger.warning(f"[{connection.config.hostname}] Bad channel key for {channel}. Cannot join.")
