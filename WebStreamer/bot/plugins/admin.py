import time
import shutil
import string
import random
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
from WebStreamer import StreamBot, Var, StartTime
from WebStreamer.utils.database import db
from WebStreamer.utils import get_readable_time, get_readable_file_size

@StreamBot.on_message(filters.command("status") & filters.private & filters.user(Var.OWNER_ID))
async def admin_status(c: Client, m: Message):
    total_users = await db.total_users_count()
    uptime = get_readable_time(time.time() - StartTime)
    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)

    await m.reply_text(
        f"**System Status**\n\n"
        f"**Uptime:** {uptime}\n"
        f"**Total Users:** {total_users}\n"
        f"**Disk Space:** {total} Total / {used} Used / {free} Free\n"
    )

@StreamBot.on_message(filters.command("broadcast") & filters.private & filters.user(Var.OWNER_ID) & filters.reply)
async def broadcast_handler(c: Client, m: Message):
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message

    success = 0
    failed = 0

    status_msg = await m.reply_text("Broadcast Started...")

    async for user in all_users:
        try:
            await broadcast_msg.copy(chat_id=user['_id'])
            success += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.1)

    await status_msg.edit_text(f"Broadcast Completed.\nSuccess: {success}\nFailed: {failed}")

@StreamBot.on_message(filters.command("add_premium") & filters.private & filters.user(Var.OWNER_ID))
async def add_premium(c: Client, m: Message):
    if len(m.command) != 3:
        return await m.reply_text("Usage: /add_premium <user_id> <gb_amount>")

    try:
        user_id = int(m.command[1])
        gb_amount = int(m.command[2])
        bytes_amount = gb_amount * 1024 * 1024 * 1024

        if not await db.is_user_exist(user_id):
            await db.add_user(user_id)

        await db.update_user_quota(user_id, bytes_amount)
        await m.reply_text(f"Added {gb_amount}GB quota to user {user_id}.")

    except ValueError:
        await m.reply_text("Invalid user ID or amount.")

@StreamBot.on_message(filters.command("genkey") & filters.private & filters.user(Var.OWNER_ID))
async def gen_key(c: Client, m: Message):
    # Usage: /genkey <amount_gb>
    if len(m.command) < 2:
        return await m.reply_text("Usage: /genkey <amount_gb>")

    type_arg = m.command[1]

    key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    try:
        amount = int(type_arg)
        bytes_amount = amount * 1024 * 1024 * 1024
        await db.create_pass_key(key, "premium", bytes_amount)
        msg = f"Generated Premium Key ({amount}GB):\n`{key}`\n\nUse /premium {key} to claim."
    except ValueError:
        return await m.reply_text("Invalid amount. Use a number for GB.")

    await m.reply_text(msg)
