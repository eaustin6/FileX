# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import time
import shutil
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message

from WebStreamer import StreamBot, Var, StartTime, __version__
from WebStreamer.bot import authorized_users
from WebStreamer.utils import get_readable_time
from WebStreamer.utils.permissions import is_user_banned, is_user_locked


@StreamBot.on_message(filters.command(["start", "help"]) & filters.private)
async def start(_, m: Message):
    if is_user_locked(m.from_user.id, m.from_user.username):
        return await m.reply(
            "This bot is in **Lock Mode**. Please authorize yourself using `/login <passkey>`.",
            quote=True
        )

    if is_user_banned(m.from_user.id, m.from_user.username):
        return await m.reply(
             "You are not in the allowed list of users who can use me. \
            ask @bearzap to use me.",
            disable_web_page_preview=True, quote=True
        )
    await m.reply(
        f'Hello {m.from_user.mention(style="md")},\n\nSend me a file & I will do the rest for you.\n\nJoin @bearzap'
    )

@StreamBot.on_message(filters.command("login") & filters.private)
async def login_handler(_, m: Message):
    if not Var.LOCK_MODE:
        return await m.reply("Lock mode is not enabled.", quote=True)

    if len(m.command) != 2:
        return await m.reply("Usage: `/login <passkey>`", quote=True)

    passkey = m.command[1]
    if passkey == Var.PASSKEY:
        authorized_users.add(m.from_user.id)
        return await m.reply("Authorization successful! You can now use the bot.", quote=True)
    else:
        return await m.reply("Invalid passkey.", quote=True)

@StreamBot.on_message(filters.command("status") & filters.private)
async def status_handler(_, m: Message):
    # Only allowed users or owner can see status? Or everyone?
    # Usually public status is fine, but maybe restricted.
    # I'll allow everyone for now unless LOCK_MODE restricts it?
    # Let's say status is public, but maybe restrict if needed.
    # But user asked for "status command", implies usability.

    uptime = get_readable_time(time.time() - StartTime)
    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    await m.reply_text(
        f"<b>Server Status:</b> Running 🟢\n"
        f"<b>Uptime:</b> {uptime}\n"
        f"<b>Current Time:</b> {current_time}\n"
        f"<b>Disk Usage:</b> {used} / {total} (Free: {free})\n"
        f"<b>Version:</b> {__version__}",
        quote=True
    )

@StreamBot.on_message(filters.command("ping") & filters.private)
async def ping_handler(_, m: Message):
    start_time = time.time()
    reply = await m.reply("Pinging...", quote=True)
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    await reply.edit_text(f"Pong! 🏓\nLatency: {latency:.2f} ms")

def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)} {["B", "KB", "MB", "GB", "TB"][index]}'
    except IndexError:
        return "File too large"
