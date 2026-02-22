# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import time
from pyrogram import filters
from pyrogram.types import Message

from WebStreamer import StreamBot, Var, StartTime, __version__
from WebStreamer.utils import get_readable_time, get_readable_file_size


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
    bandwidth = get_readable_file_size(Var.BytesServed)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    await m.reply_text(
        f"<b>Server Status:</b> Running\n"
        f"<b>Version:</b> {__version__}\n"
        f"<b>Uptime:</b> {uptime}\n"
        f"<b>Bandwidth Used:</b> {bandwidth}\n"
        f"<b>Date:</b> {current_time}",
        quote=True
    )

@StreamBot.on_message(filters.command("ping") & filters.private)
async def ping(_, m: Message):
    start_time = time.time()
    reply = await m.reply_text("Pinging...", quote=True)
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    await reply.edit_text(f"Pong! 🏓\nLatency: {latency:.2f} ms")

@StreamBot.on_message(filters.command("login") & filters.private)
async def login(_, m: Message):
    if not Var.LOCK_PASSWORD:
        return await m.reply_text("Lock mode is not enabled.", quote=True)

    if len(m.command) != 2:
        return await m.reply_text("Usage: /login <password>", quote=True)

    password = m.command[1]
    if password == Var.LOCK_PASSWORD:
        Var.AUTH_USERS.add(m.from_user.id)
        await m.reply_text("Login successful! You can now use the bot.", quote=True)
    else:
        await m.reply_text("Incorrect password.", quote=True)
