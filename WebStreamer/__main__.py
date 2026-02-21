# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import asyncio
import logging
import sys

from aiohttp import web
from pyrogram import idle

from WebStreamer import StreamBot, utils
from WebStreamer.bot.clients import initialize_clients
from WebStreamer.server import web_server

from .vars import Var

logging.basicConfig(
    level=logging.DEBUG if Var.DEBUG else logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="[%(asctime)s][%(name)s][%(levelname)s] ==> %(message)s",
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
        logging.FileHandler("streambot.log", mode="a", encoding="utf-8"),
    ],
)

logging.getLogger("aiohttp").setLevel(logging.DEBUG if Var.DEBUG else logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.INFO if Var.DEBUG else logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.DEBUG if Var.DEBUG else logging.ERROR)

server = web.AppRunner(web_server())

async def start_services():
    logging.info("Initializing Telegram Bot")
    await StreamBot.start()
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    logging.info(f"Initialized Telegram Bot: {bot_info.first_name}")

    await initialize_clients()

    if Var.KEEP_ALIVE:
        asyncio.create_task(utils.ping_server())

    await server.setup()
    await web.TCPSite(server, Var.BIND_ADDRESS, Var.PORT).start()
    logging.info("Service Started")
    if bot_info.dc_id:
        logging.info(f"DC ID =>> {bot_info.dc_id}")
    logging.info(f"URL =>> {Var.URL}")

    await idle()

async def cleanup():
    await server.cleanup()
    await StreamBot.stop()

async def main():
    try:
        await start_services()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.error(f"Error: {err}", exc_info=True)
    finally:
        await cleanup()
        logging.info("Stopped Services")

if __name__ == "__main__":
    asyncio.run(main())
