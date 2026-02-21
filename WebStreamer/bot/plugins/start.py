# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import time
from pyrogram import filters
from pyrogram.types import Message

from WebStreamer import StreamBot, Var, StartTime, __version__
from WebStreamer.utils import get_readable_time


@StreamBot.on_message(filters.command(["start", "help"]) & filters.private)
async def start(_, m: Message):
    if Var.ALLOWED_USERS and not ((str(m.from_user.id) in Var.ALLOWED_USERS) or (m.from_user.username in Var.ALLOWED_USERS)):
        return await m.reply(
             "You are not in the allowed list of users who can use me. \
            ask @bearzap to use me.",
            disable_web_page_preview=True, quote=True
        )
    await m.reply(
        f'Hello {m.from_user.mention(style="md")},\n\nSend me a file & I will do the rest for you.\n\nJoin @bearzap'
    )

@StreamBot.on_message(filters.command("status") & filters.private)
async def status(_, m: Message):
    uptime = get_readable_time(time.time() - StartTime)
    await m.reply_text(
        f"<b>Server Status:</b> Running\n"
        f"<b>Uptime:</b> {uptime}\n"
        f"<b>Version:</b> {__version__}",
        quote=True
    )
