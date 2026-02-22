# This file is a part of TG-FileStreamBot
# Coding : Owner

from pyrogram import filters, Client
from pyrogram.types import Message
from WebStreamer import StreamBot, Var
from WebStreamer.utils.database import db
from WebStreamer.utils.permissions import is_user_banned
from WebStreamer.utils import get_readable_file_size

@StreamBot.on_message(filters.command(["start", "help"]) & filters.private)
async def start(c: Client, m: Message):
    if is_user_banned(m.from_user.id, m.from_user.username):
        return await m.reply(
             "You are not in the allowed list of users who can use me. \
            ask @bearzap to use me.",
            disable_web_page_preview=True, quote=True
        )

    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)

    await m.reply_text(
        f"Hello {m.from_user.mention},\n\n"
        "Send me a file and I will generate a direct download link for you!\n\n"
        "Use /status to check your quota.\n"
        "Use /premium to buy more quota."
    )

@StreamBot.on_message(filters.command("status") & filters.private)
async def status_handler(c: Client, m: Message):
    user_data = await db.get_user(m.from_user.id)
    if not user_data:
        await db.add_user(m.from_user.id)
        user_data = await db.get_user(m.from_user.id)

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
    if len(m.command) == 2:
        key = m.command[1]
        pass_key = await db.get_pass_key(key)

        if not pass_key:
            await m.reply_text("Invalid Premium Key.")
            return

        if pass_key['type'] == 'premium':
            user_id = m.from_user.id
            if not await db.is_user_exist(user_id):
                await db.add_user(user_id)

            amount = pass_key['value']
            await db.update_user_quota(user_id, amount)
            gb = amount / (1024 * 1024 * 1024)
            await m.reply_text(f"Premium Activated! Added {gb}GB to your quota.")
            await db.delete_pass_key(key)
        else:
            await m.reply_text("Invalid Key Type.")
    else:
        await m.reply_text(
            "**Premium Plans**\n\n"
            "To increase your quota, please contact the owner to buy a key.\n"
            "Once you have a key, use `/premium <key>` to redeem it.\n\n"
            "Unlimited usage is available for the owner only.\n\n"
            "Contact: @Owner"
        )
