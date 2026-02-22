# This file is a part of TG-FileStreamBot
# Coding : Owner

import time
from pyrogram import filters, Client
from pyrogram.types import Message
from WebStreamer import StreamBot, Var, StartTime
from WebStreamer.utils.database import db
from WebStreamer.utils import get_readable_time
from WebStreamer.utils.permissions import is_user_banned, is_user_locked

@StreamBot.on_message(filters.command(["start", "help"]) & filters.private)
async def start(c: Client, m: Message):
    if not await db.is_user_exist(m.from_user.id):
        if Var.LOCK_MODE:
             # Check if user has an "Access" key or Premium?
             # For now, if Lock Mode is on, we don't add user automatically.
             # We ask them to login.
             await m.reply_text(
                 f"Hello {m.from_user.mention},\n\n"
                 "This bot is in **Lock Mode**.\n"
                 "Please use `/login <passkey>` to access the bot.\n"
                 "Contact the owner if you don't have a key."
             )
             return
        else:
            await db.add_user(m.from_user.id)
    else:
        # User exists.
        pass

    await m.reply_text(
        f"Hello {m.from_user.mention},\n\n"
        "Send me a file and I will generate a direct download link for you!\n\n"
        "Use /status to check your quota.\n"
        "Use /premium to buy more quota."
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
async def login_handler(c: Client, m: Message):
    if len(m.command) != 2:
        return await m.reply_text("Usage: `/login <passkey>`")

    key = m.command[1]
    pass_key = await db.get_pass_key(key)

    if not pass_key:
        return await m.reply_text("Invalid Pass Key.")

    user_id = m.from_user.id

    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)

    # Process Key
    if pass_key['type'] == 'access':
        await m.reply_text("Access Granted! You can now use the bot.")
    elif pass_key['type'] == 'premium':
        amount = pass_key['value']
        await db.update_user_quota(user_id, amount)
        gb = amount / (1024 * 1024 * 1024)
        await m.reply_text(f"Premium Activated! Added {gb}GB to your quota.")

    # Delete used key
    await db.delete_pass_key(key)

@StreamBot.on_message(filters.command("status") & filters.private)
async def status_handler(c: Client, m: Message):
    user_data = await db.get_user(m.from_user.id)
    if not user_data:
        await m.reply_text("You are not registered. Use /start.")
        return

    quota = user_data['quota']
    used = user_data['used']

    if m.from_user.id == Var.OWNER_ID:
        quota_str = "Unlimited"
        remaining_str = "Unlimited"
    else:
        quota_str = get_readable_file_size(quota)
        remaining = quota - used
        remaining_str = get_readable_file_size(remaining)

    used_str = get_readable_file_size(used)

    await m.reply_text(
        f"**User Status**\n\n"
        f"**Quota:** {quota_str}\n"
        f"**Used:** {used_str}\n"
        f"**Remaining:** {remaining_str}\n\n"
        "Buy Premium: /premium"
    )

@StreamBot.on_message(filters.command("premium") & filters.private)
async def premium_handler(c: Client, m: Message):
    await m.reply_text(
        "**Premium Plans**\n\n"
        "To increase your quota, please contact the owner.\n"
        "Unlimited usage is available for the owner only.\n\n"
        "Contact: @Owner (Replace with actual username if known or keep generic)"
    )

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
