# This file is a part of TG-FileStreamBot

from pyrogram import filters
from pyrogram.types import Message

from WebStreamer import StreamBot, Var
from WebStreamer.utils.database import db

@StreamBot.on_message(filters.command("broadcast") & filters.private & filters.user(Var.OWNER_ID))
async def broadcast_handler(_, m: Message):
    if not m.reply_to_message:
        return await m.reply("Reply to a message to broadcast.", quote=True)

    users = await db.get_all_users()
    count = 0
    async for user in users:
        try:
            await m.reply_to_message.copy(chat_id=user['id'])
            count += 1
        except Exception:
            pass

    await m.reply(f"Broadcasted to {count} users.", quote=True)

@StreamBot.on_message(filters.command("add_premium") & filters.private & filters.user(Var.OWNER_ID))
async def add_premium_handler(_, m: Message):
    if len(m.command) != 3:
        return await m.reply("Usage: `/add_premium <user_id> <limit_bytes>`", quote=True)

    user_id = int(m.command[1])
    limit = int(m.command[2])

    await db.add_premium(user_id, limit)
    await m.reply(f"Added premium to user {user_id} with limit {limit} bytes.", quote=True)

@StreamBot.on_message(filters.command("remove_premium") & filters.private & filters.user(Var.OWNER_ID))
async def remove_premium_handler(_, m: Message):
    if len(m.command) != 2:
        return await m.reply("Usage: `/remove_premium <user_id>`", quote=True)

    user_id = int(m.command[1])
    await db.remove_premium(user_id)
    await m.reply(f"Removed premium from user {user_id}.", quote=True)

@StreamBot.on_message(filters.command("generate_key") & filters.private & filters.user(Var.OWNER_ID))
async def generate_key_handler(_, m: Message):
    if len(m.command) < 2:
        return await m.reply("Usage: `/generate_key <key> [description]`", quote=True)

    key = m.command[1]
    desc = " ".join(m.command[2:]) if len(m.command) > 2 else ""

    await db.create_access_key(key, desc)
    await m.reply(f"Access key `{key}` created.", quote=True)
