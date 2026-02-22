# This file is a part of TG-FileStreamBot
# Coding : Owner

import asyncio
from urllib.parse import quote_plus
from pyrogram import filters, Client
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from WebStreamer import StreamBot, Var
from WebStreamer.utils.database import db
from WebStreamer.utils import get_hash, get_name
from WebStreamer.utils.permissions import is_user_banned

@StreamBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ),
    group=4,
)
async def media_receive_handler(c: Client, m: Message):
    if is_user_banned(m.from_user.id, m.from_user.username):
        return await m.reply(
             "You are not in the allowed list of users who can use me. \
            ask @bearzap to use me.",
            disable_web_page_preview=True, quote=True
        )

    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)

    user = await db.get_user(m.from_user.id)

    if m.from_user.id != Var.OWNER_ID and user['used'] >= user['quota']:
        return await m.reply_text(
            "**Quota Exceeded**\n\n"
            "You have used all your allocated data.\n"
            "Please upgrade your plan using /premium."
        )

    try:
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)

        file_hash = get_hash(log_msg, Var.HASH_LENGTH, m.from_user.id)
        file_name = get_name(log_msg)

        stream_link = f"{Var.URL}{log_msg.id}/{quote_plus(file_name)}?hash={file_hash}&id={m.from_user.id}"
        short_link = f"{Var.URL}{file_hash}{log_msg.id}?id={m.from_user.id}"

        await m.reply_text(
            text="<code>{}</code>\n(<a href='{}'>shortened</a>)".format(
                stream_link, short_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔴 Download Link", url=stream_link)],
                    [InlineKeyboardButton("🟢 Watch Online", url=stream_link)],
                    [InlineKeyboardButton("🔵 Short Link", url=short_link)]
                ]
            ),
        )
    except Exception as e:
        await m.reply_text(f"Something went wrong!\n\nError: {e}")
