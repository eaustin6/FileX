# This file is a part of TG-FileStreamBot

import time
import shutil
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from WebStreamer import StreamBot, Var, StartTime, __version__
from WebStreamer.utils import get_readable_time
from WebStreamer.utils.database import db

@StreamBot.on_message(filters.command(["start", "help"]) & filters.private)
async def start(_, m: Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await m.reply_text(
            f"Hello {m.from_user.mention(style='md')},\n\nI am a File Stream Bot. Send me any file and I will give you a direct download link."
        )

    # Lock Mode Check
    if Var.LOCK_MODE:
        user = await db.get_user(m.from_user.id)
        if not user or not user.get('authorized', False):
             if not (str(m.from_user.id) in Var.ALLOWED_USERS or m.from_user.username in Var.ALLOWED_USERS or m.from_user.id == Var.OWNER_ID):
                return await m.reply(
                    "This bot is in **Lock Mode**. Please authorize yourself using `/login <passkey>`.",
                    quote=True
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

    # Check Database Key first
    db_key = await db.get_access_key(passkey)
    if db_key:
        await db.use_access_key(passkey, m.from_user.id)
        # Mark user as authorized in their record
        await db.col.update_one({'id': m.from_user.id}, {'$set': {'authorized': True}})
        return await m.reply("Authorization successful! You can now use the bot.", quote=True)

    # Check Env Key (Master Key)
    if passkey == Var.PASSKEY:
        await db.col.update_one({'id': m.from_user.id}, {'$set': {'authorized': True}})
        return await m.reply("Authorization successful! You can now use the bot.", quote=True)

    return await m.reply("Invalid passkey.", quote=True)

@StreamBot.on_message(filters.command("status") & filters.private)
async def status_handler(_, m: Message):
    uptime = get_readable_time(time.time() - StartTime)
    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    user_data = await db.get_user(m.from_user.id)
    if not user_data:
        await db.add_user(m.from_user.id)
        user_data = await db.get_user(m.from_user.id)

    traffic_used = get_readable_file_size(user_data.get('traffic_used', 0))
    traffic_limit = user_data.get('traffic_limit', 0)

    if m.from_user.id == Var.OWNER_ID:
        limit_text = "Unlimited (Owner)"
    elif traffic_limit == 0:
        limit_text = "Standard Limit" # Or whatever default logic
    else:
        limit_text = get_readable_file_size(traffic_limit)

    await m.reply_text(
        f"<b>Server Status:</b> Running 🟢\n"
        f"<b>Uptime:</b> {uptime}\n"
        f"<b>Current Time:</b> {current_time}\n"
        f"<b>Disk Usage:</b> {used} / {total} (Free: {free})\n"
        f"<b>Version:</b> {__version__}\n\n"
        f"<b>User Stats:</b>\n"
        f"<b>ID:</b> <code>{m.from_user.id}</code>\n"
        f"<b>Traffic Used:</b> {traffic_used}\n"
        f"<b>Traffic Limit:</b> {limit_text}",
        quote=True
    )

@StreamBot.on_message(filters.command("ping") & filters.private)
async def ping_handler(_, m: Message):
    start_time = time.time()
    reply = await m.reply("Pinging...", quote=True)
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    await reply.edit_text(f"Pong! 🏓\nLatency: {latency:.2f} ms")

@StreamBot.on_message(filters.command("premium") & filters.private)
async def premium_handler(_, m: Message):
    # Show owner contact info for buying premium
    # In a real scenario, this might be fetched from DB or Var
    owner_id = Var.OWNER_ID
    text = "To buy premium or increase your quota, please contact the owner."
    if owner_id:
        try:
            owner = await StreamBot.get_users(owner_id)
            text += f"\n\nOwner: {owner.mention}"
        except Exception:
            text += f"\n\nOwner ID: <code>{owner_id}</code>"

    await m.reply(text, quote=True)


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
